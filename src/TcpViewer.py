import os, traceback, shutil, Queue, re, uuid 
import Utilities as utils

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from datetime import datetime
from threading import Thread
from time import sleep
from PIL import Image

from TcpflowWrapper import TcpflowWrapper

class OutputDirectoryListener(FileSystemEventHandler):
    
    # http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html
    image_extensions = ['jpeg', 'jpg'] # gif crashes

    def __init__(self, observer, image_extraction_queue):
        self.image_extraction_queue = image_extraction_queue
        self.directory_observer = observer

    def on_created(self, event):
        if not event.is_directory:
            filename = event.src_path[event.src_path.rfind('/') + 1:]
            extension = filename[filename.rfind('.') + 1:]

            if extension in self.image_extensions:
                self.image_extraction_queue.put(event.src_path)

    def on_modified(self, event): pass
    def on_deleted(self, event): pass

    def stop_observer(self):
        self.directory_observer.stop()

class TcpViewer():

    directory_observer = Observer()
    image_extraction_queue = Queue.Queue()
    
    extraction_interval = None
    min_width = 500
    min_height = 500

    def __init__(self, verbose, interface, exclude_ips, clean, output_dir, frontend, address):
        self.verbose = verbose
        self.exclude_ips = exclude_ips
        
        if frontend and address:
            output_dir, frontend_command = self.arrange_frontend(frontend, address)
        else:
            self.db_path = os.path.join(output_dir, 'database.db')
        
        self.output_dir = output_dir 
        self.raw_dir = os.path.join(output_dir, 'raw')
        self.images_dir = os.path.join(output_dir, 'images')

        if clean: self.clean_workspace()

        self.init_directories()
        self.init_sqlite_db()
        self.start_output_dir_listener()

        if frontend:
            print 'Starting the %s frontend at http://%s.' % (frontend, address)
            utils.start_subprocess(frontend_command, True) # needs db

        self.start_threads(True)

        self.tcpflow = TcpflowWrapper(verbose)
        self.xml_report_path = os.path.join(self.raw_dir, 'report.xml')
        self.tcpflow.as_main_process(interface, self.raw_dir)

    def arrange_frontend(self, frontend, address):
        output_location = command = None

        if frontend == 'nodejs':
            output_location = os.path.join(os.getcwd(), 'frontend/nodejs/public/')
            output_dir = os.path.join(output_location, 'output/')
            self.db_path = os.path.join(output_dir, 'database.db')
            command = 'nodejs frontend/nodejs/app.js -a %s -d %s' % (address, self.db_path)
        else:
            raise ValueError('The frontend %s was not found at its location.' % frontend)
        
        if os.path.exists(output_location) == False:
            raise ValueError('The %s output location %s does not exist.' % (frontend, output_location))
        
        return output_dir, command

    def clean_workspace(self):
        if os.path.exists(self.output_dir): 
            shutil.rmtree(self.output_dir)
            os.mkdir(self.output_dir)

    def init_directories(self):
        if os.path.exists(self.output_dir) == False:
            os.mkdir(self.output_dir)

        if os.path.exists(self.raw_dir) == False:
            os.mkdir(self.raw_dir)

        if os.path.exists(self.images_dir) == False:
            os.mkdir(self.images_dir)

    def init_sqlite_db(self):
        command = '''CREATE TABLE IF NOT EXISTS IMAGES(
            HASH TEXT,
            TIMESTAMP DATE,
            SMAC TEXT,
            DMAC TEXT,
            SIP TEXT,
            DIP TEXT
        );
        '''
        utils.execute_sqlite3_cmd(self.db_path, command)

    def start_output_dir_listener(self):
        event_handler = OutputDirectoryListener(
            self.directory_observer,
            self.image_extraction_queue
        )
        self.directory_observer.schedule(
            event_handler,
            self.raw_dir,
            recursive = False
        )
        self.directory_observer.start()

    def start_threads(self, as_daemon):
        '''
            if as_daemon: quits without waiting for the threads to finish.
        '''
        thread = Thread(target = self.image_extraction_queue_listener, args=[])
        thread.daemon = as_daemon
        thread.start()

    def insert_to_sqlite_db(self, file_uuid, src, dst, macs, ips):
        command = ('INSERT INTO IMAGES Values(' +
            utils.quotes_wrap(file_uuid) + ',' +
            utils.quotes_wrap(datetime.now()) + ',' +
            utils.quotes_wrap(macs[0]) + ',' +
            utils.quotes_wrap(macs[1]) + ',' +
            utils.quotes_wrap(ips[0]) + ',' +
            utils.quotes_wrap(ips[1]) + ');'
        )
        utils.execute_sqlite3_cmd(self.db_path, command)

    def image_extraction_queue_listener(self):
        while True:
            try:
                filepath = self.image_extraction_queue.get()
                image = Image.open(filepath)
                width, height = image.size

                if width < self.min_width or height < self.min_height:
                    continue

                filename = filepath[filepath.rfind('/') + 1:]
                file_uuid = str(uuid.uuid4())
                src = os.path.abspath(os.path.join(self.raw_dir, filename))
                dst = os.path.abspath(os.path.join(self.images_dir, file_uuid + '.jpg'))

                try:
                    macs = self.tcpflow.get_macs_from_report(filepath, self.xml_report_path)
                    ips, exclude = self.tcpflow.get_ips_from_filepath(filepath, self.exclude_ips)
                    if exclude:
                        print 'Excluding packets from %s to %s.' % (ips[0], ips[1])
                        continue
                except ValueError as e:
                    if self.verbose: print e

                self.insert_to_sqlite_db(file_uuid, src, dst, macs, ips)

                if self.verbose:
                    print 'Got an image higher than %sx%s minimum. Moving %s --> %s.' % (
                        self.min_width, self.min_height, src, dst)

                # overwrites existing, otherwise use .copy2()
                shutil.move(src, dst)

            except (Queue.Empty, IOError) as e:
                traceback.print_exc()

