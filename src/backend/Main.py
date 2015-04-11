"""
	Main class wrapping network interceptors tools.
"""

import os, subprocess, shutil, Queue

# pill watchdog
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class OutputDirectoryListener(FileSystemEventHandler):
   """Private class"""

   # http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html
   image_extensions = ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'im']

   def __init__(self, observer, image_extraction_queue):
      self.image_extraction_queue = image_extraction_queue
      self.directory_observer = observer

   def on_created(self, event):
      if not event.is_directory:
         filename = event.src_path[event.src_path.rfind('/') + 1:]
         extension = filename[filename.rfind('.') + 1:]

         if extension in self.image_extensions:
            self.image_extraction_queue.put(event.src_path)

   def on_modified(self, event):
      pass

   def on_deleted(self, event):
      pass

   def stop_observer(self):
      self.directory_observer.stop()

class Main():

	directory_observer = Observer()
	image_extraction_queue = Queue.Queue()
	extraction_interval = None

	min_width = 500
	min_height = 500

	def __init__(self, interface, output, clean):
		self.output_dir = output
		self.raw_dir = os.path.join(output, 'raw')
		self.images_dir = os.path.join(output, 'images')

		self.init_directories(clean)

		self.start_output_dir_listener()

		self.tcpflow_as_main_process(interface)


	def init_directories(self, clean):
		if os.path.exists(self.output_dir) == False:
			os.mkdir(self.output_dir)
		elif clean:
			shutil.rmtree(self.output_dir)
			os.mkdir(self.output_dir)

		if os.path.exists(self.raw_dir) == False:
			os.mkdir(self.raw_dir)

		if os.path.exists(self.images_dir) == False:
			os.mkdir(self.images_dir)

	def start_loud_subprocess(self, command):
		return subprocess.Popen(command,
			shell = True,
			stdout = subprocess.PIPE, 
			stderr = subprocess.STDOUT
		)

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

	def tcpflow_as_main_process(self, interface):
		"""
			tcpflow related variables and the commmand for main process.
		"""
		self.xml_report_path = os.path.join(self.raw_dir, 'report.xml')
		tcpflow = 'sudo tcpflow -i ' + interface + ' -e http -o ' + self.raw_dir
		
		try:
			proc = self.start_loud_subprocess(tcpflow)

			while proc.poll() is None:
				print proc.stdout.readline()

		except KeyboardInterrupt:
			print "Got Keyboard interrupt. Stopping..."
