#!/usr/bin/python3

import signal
import tix_lib
from time import sleep
import random

def signal_handler(signal, frame):
	print("\033[?25h")
	sys.exit(0)

print("\033[?25l", end="")
signal.signal(signal.SIGINT, signal_handler)
while True:
	g=tix_lib.get_time()
	tix_lib.update(g[0] % 12, g[1])
	sleep(random.randrange(0,10)/10+2.5)
	tix_lib.go_back_up_three_lines()
