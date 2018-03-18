#!/usr/bin/python3

import signal
import tix_lib
from time import sleep
import random
import sys
import parameters


def signal_handler(signal, frame):
	print("\033[?25h")
	print("\033[%dE" % 3*(parameters.block_vert_space+1))
	sys.exit(0)

def run():
	print("\033[?25l", end="") # remove cursor
	signal.signal(signal.SIGINT, signal_handler)
	blocks=None
	time=None
	inc=0
	while True:
		time,changed=tix_lib.get_time(old_time=time, format_=12)
		columns_to_update=[]
		if parameters.style in [2, 3]:
			if 0 in changed:
				columns_to_update.append(0)
				columns_to_update.append(1)
			if 1 in changed:
				columns_to_update.append(2)
				columns_to_update.append(3)
			if changed==[]:
				if parameters.style==3:
# for that style, we don't update empty blocked
					if inc==0:
						if time[0]<10:
							inc=inc+1
					if inc==2:
						if time[1]<10:
							inc=inc+1
				columns_to_update=[inc]
				
				inc=(inc+1)%4
			delay=0.5

		if parameters.style==1:
			columns_to_update=[0,1,2,3] 
			delay=random.randrange(0,10)/10+2.5

		s=""
		for column in columns_to_update: 
			blocks=tix_lib.update(hour=time[0], minute=time[1], blocks=blocks, section_to_refresh=column, add=parameters.style==3)
			s=s+tix_lib.print_block(column, blocks[column])
		print(s, end="") 
		sleep(delay) 

run()
