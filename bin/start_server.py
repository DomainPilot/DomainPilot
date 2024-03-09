#!/usr/bin/env python3

# This script start a uwsgi server and utilizes watchdog library to monitor changes 
# on the domain_pilot directory, reloading server, if it detects changes on the files

import subprocess
from time import sleep
from watchdog.observers import Observer
from shutil import which

if which('uwsgi') == None:
	print("ERROR: You need to have uwsgi installed!")
	print("Try installing it with:")
	print("sudo apt install uwsgi uwsgi-plugin-python3")
	quit()

changes = False
class events():
	def dispatch(event):
		if event.event_type in ['modified', 'created', 'deleted']:
			global changes
			changes=True

command  = "uwsgi --plugins python3,http --master-fifo /tmp/uwsgi_fifo "
command += "--http :9090 -H .venv --wsgi-file domain_pilot --logto2 server.log"
server = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print(f'Server is running with pid {server.pid}...')

observer = Observer()
observer.schedule(events, 'domain_pilot', recursive=True)  
observer.start() 
try:
	while True:
		if changes == True:
			changes = False
			print("Files changed... Reloading server!")
			subprocess.run('echo R > /tmp/uwsgi_fifo', shell=True)
		sleep(1)
except KeyboardInterrupt:
	observer.stop()
	observer.join()
	print("\nTerminating the server...")
	subprocess.run('echo Q > /tmp/uwsgi_fifo', shell=True)
	subprocess.run('rm /tmp/uwsgi_fifo', shell=True)
