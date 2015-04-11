"""
	Main class wrapping network interceptors tools.
"""

import os, subprocess, shutil, Queue
# pill watchdog
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

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
