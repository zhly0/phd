import os
import subprocess 
from random import randint
import threading
import shutil

workspace = ""
results_file_path = "/home/ycinar/pesq_results"
test_command = ""

def prep_env():
	global workspace
	global test_command

	if os.path.isdir("/home/ycinar/dev/src/out/Debug/"):
		workspace = "/home/ycinar/dev/src/out/Debug/"
	elif os.path.isdir("/home/ycinar/okul/src/out/Debug/"):
		workspace = "/home/ycinar/okul/src/out/Debug/"
	else:
		print "workspace is not found - script will fail"
	print "workspace: ", workspace	
	test_command = workspace + "browser_tests --gtest_filter=WebrtcAudioQualityBrowserTest.MANUAL_TestAudioQuality --single_process"

	# remove the results file
	try:
		os.remove(results_file_path)
	except OSError:
		pass
		
	open(results_file_path, 'a').close()

def execute_test():
	# execute the tests
	print test_command
	for x in range(0,1):
		print "Start the test no:%d" % (x)
		subprocess.call([test_command], shell=True)
		print "Completed the test..."

def add_header_for_test_case(header):
	results_file = open(results_file_path, "a")
	results_file.write(header)
	results_file.close()

class netem_jitter_thread(threading.Thread):
	def __init__(self, name):
		threading.Thread.__init__(self)
		#self.threadID = threadID
		self.name = name
		self.shutdown = False
	def run(self):
		print "Starting " + self.name
		while not self.shutdown:
			execute_netem()
		print "Exiting " + self.name

def execute_netem():
	delay = randint(50,500)
	netem_command = "sudo tc qdisc change dev lo root handle 1: netem delay %dms" % delay
	subprocess.call([netem_command], shell=True)

def run_scenarios():
	# add header
	#add_header_for_test_case("Results with no network config\n")

	netem_thread = netem_jitter_thread('netem_thread')
	netem_thread.start()

	# execute the tests
	execute_test()
	netem_thread.shutdown = True
	netem_thread.join()

	'''
	# change the network config
	subprocess.call(["sudo tc qdisc add dev lo root netem delay 100ms 50ms"], shell=True)
	add_header_for_test_case("Results with 100ms 50ms\n")
	execute_test()
	
	subprocess.call(["sudo tc qdisc add dev lo root netem delay 100ms 100ms"], shell=True)
	add_header_for_test_case("Results with 100ms 100ms\n")
	execute_test()

	subprocess.call(["sudo tc qdisc add dev lo root netem delay 100ms 150ms"], shell=True)
	add_header_for_test_case("Results with 100ms 150ms\n")
	execute_test()
	'''

def report_results():
	#open the file
	with open(results_file_path, "r") as results_file:
		for line in results_file:
			print line

	results_file.close()
	shutil.copy(results_file_path, '.')

if __name__ == '__main__':
	prep_env()
	run_scenarios()
	report_results()
	subprocess.call(["sudo tc qdisc del dev lo root"], shell=True)