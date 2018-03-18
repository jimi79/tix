import datetime
import random

use_256_colors=True

tab="    " # at the beginning of the clock for each line
space="  " # between blocks
led="  " # size of a led
led_space=" " # space between leds
lines=1 # space between lines
if use_256_colors:
	colors=[124, 34, 21, 124]
	colors=["\033[48;5;%dm" % c for c in colors]
	empty_cell_color="\033[48;5;233m"
else:
	colors=[41, 42, 44, 41]
	colors=["\033[%dm" % c for c in colors]
	empty_cell_color="\033[40m"


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

	for i in range(0, 3):
		for l in range(0, lines):
			print("")
		print(tab, end="")
		for j in range(0, len(blocks)):
			b=blocks[j]
			color=colors[j]
			for k in range(0, b['size']):
				l=k+i*b['size']
				if l in b['val']:
					print("%s%s" % (color, led), end="")
				else:
					print("%s%s" % (empty_cell_color, led), end="")
				print("\033[40m%s" % led_space, end="")
				#print( )
			print("\033[40m%s" % space, end="")
		print("\33[0m")
	return blocks


def get_time():
	now=datetime.datetime.now()
	hour=now.hour
	minute=now.minute
	return [hour, minute]

def go_back_up_three_lines():
	a=3*(1+lines)
	print("\033[%dA" % a, end="")


