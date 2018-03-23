#!/usr/bin/python3.5

import signal
from tix_lib import *
from time import sleep
import random
import sys
import parameters


def signal_handler(signal, frame):
	print("\033[?25h")
	#print("\033[%dE" % 3*(parameters.block_vert_space+1))
	sys.exit(0)

def run():
	print("\033[?25l", end="") # remove cursor
	signal.signal(signal.SIGINT, signal_handler)
	blocks=None
	time=None
	inc=0
	while True:
		time, blocks, stdout, delay=update_display(time, blocks)
		print(stdout, end="")
		sleep(delay)

run()
