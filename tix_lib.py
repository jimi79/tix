import datetime
import random
from time import sleep

tab="    " # at the beginning of the clock for each line
space="  " # between blocks

def get_array(val, cols):
	c=[i for i in range(0,3*cols)]
	d=[]
	for i in range(0,val):
		d.append(c.pop(random.randrange(len(c))))
	return {'val': d, 'size': cols}


def update(hour, minute): 

	blocks=[]
	blocks.append(get_array(int(hour/10), 1))
	blocks.append(get_array(hour%10, 3))
	blocks.append(get_array(int(minute/10), 2))
	blocks.append(get_array(minute%10, 3))

	colors=[31, 32, 34, 31]
	for i in range(0, 3):
		print(tab, end="")
		for j in range(0, len(blocks)):
			b=blocks[j]
			color=colors[j]
			print("\033[%dm" % color, end="")
			for k in range(0, b['size']):
				l=k+i*b['size']
				if l in b['val']:
					print("#", end="")
				else:
					print(" ", end="")
				#print( )
			print(space, end="")
		print("\33[0m")
	return blocks


def get_time():
	now=datetime.datetime.now()
	hour=now.hour
	minute=now.minute
	return [hour, minute]

def go_back_up_three_lines():
	print("\033[3A", end="")


