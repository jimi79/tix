import datetime
import random
import parameters
import shutil

if parameters.use_256_colors:
	colors=[124, 34, 21, 124]
	esc_colors=["\033[48;5;%dm" % c for c in colors]
	esc_empty_cell_color="\033[48;5;233m"
else:
	colors=[41, 42, 44, 41]
	esc_colors=["\033[%dm" % c for c in colors]
	esc_empty_cell_color="\033[40m"

# init 
block_str=""
for i in range(0, parameters.led_width):
	block_str=block_str+" "

def get_center():
	a=shutil.get_terminal_size()
	c=a.columns
	l=a.lines
	s=parameters.section_widths
	w=sum(s) * (parameters.led_width + parameters.led_space) # the width of all leds
	w=w + len(s) * parameters.block_vert_space # space between blocks
	h=3 * (parameters.block_horz_space + 1) # block size is globally fixed vertically
	X=int(c/2-w/2)
	Y=int(l/2-h/2)
	return {'X':X, 'Y' :Y}

def get_array(val, cols):
	c=[i for i in range(0,3*cols)]
	d=[]
	for i in range(0,val):
		d.append(c.pop(random.randrange(len(c))))
	return d 

def get_cursor_pos_so_that_clock_is_centered():
	# return the position of the cursor
# i have to get the screen's size, maybe each time
	pass

def update(hour, minute, blocks, section_to_refresh):
	if blocks==None:
		blocks=[None, None, None, None]
	if section_to_refresh==None or section_to_refresh==0:
		blocks[0]=get_array(int(hour/10), parameters.section_widths[0])
	if section_to_refresh==None or section_to_refresh==1:
		blocks[1]=get_array(hour%10, parameters.section_widths[1])
	if section_to_refresh==None or section_to_refresh==2:
		blocks[2]=get_array(int(minute/10), parameters.section_widths[2])
	if section_to_refresh==None or section_to_refresh==3:
		blocks[3]=get_array(minute%10, parameters.section_widths[3]) 
	return blocks	

def print_block(section, block, X, Y):
	output="" # we clear the screen
	for i in range(0, section): # calculating space before top left of the block to print
		section_width=parameters.section_widths[i]
		X=X+section_width*parameters.led_width+(section_width*parameters.led_space)+parameters.block_vert_space
	output="\033[%d;1H" % (Y+1) 

	count_added_lines=0 # number of 
	section_width=parameters.section_widths[section]
	for i in range(0, 3): # for each line
		for j in range(0, section_width):
			val=section_width*i+j
			if val in block:
				color=esc_colors[section]
			else:
				color=esc_empty_cell_color
			left=X+j*(parameters.led_width + parameters.led_space)
			output=output+color+"\033[%dG" % left
			output=output+"%s%s" % (color, block_str)
		output=output+"\n"
		count_added_lines=count_added_lines+1
		for i in range(0, parameters.block_horz_space):
			output=output+"\n"
			count_added_lines=count_added_lines+1 
	# we got to put the cursor n lines up now
	#output=output+("\033[%dF" % count_added_lines)  # might not be necessary, not sure though
	output=output+("\033[0m") 
	return output

def print_blocks(time, blocks, X, Y): 
#def update(hour, minute, blocks, section_to_refresh, add):
	blocks=update(time[0], time[1], blocks, None)
	s="\033[2J"
	s=s+"\033[0;0H" # we put cursor top left, we'll change that later
	for i, block in zip(range(0, len(blocks)), blocks):
		s=s+print_block(i, block, X, Y)
	return s

def get_time(old_time, format_):
	now=datetime.datetime.now()
	hour=now.hour
	minute=now.minute
	if format_==12:
		hour=hour % 12
	changed=[]
	if old_time!=None:
		if old_time[0] != hour:
			changed.append(0)
		if old_time[1] != minute:
			changed.append(1)
	else:
		changed=[0,1,2,3]
	return [[hour, minute], changed]


def update_display(time, blocks): 
	delay=random.randrange(0,10)/10+2.5 
	time, changed=get_time(old_time=time, format_=12)
	center=get_center()
	stdout=print_blocks(time, blocks, center['X'], center['Y']) 
	return time, blocks, stdout, delay 
	


