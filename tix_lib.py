import datetime
import random
import parameters

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

def update(hour, minute, blocks, section_to_refresh, add):
	if blocks==None:
		blocks=[None, None, None, None]
	if section_to_refresh==None or section_to_refresh==0:
		blocks[0]=get_array(int(hour/10) + add, parameters.section_widths[0])
	if section_to_refresh==None or section_to_refresh==1:
		blocks[1]=get_array(hour%10 + add, parameters.section_widths[1])
	if section_to_refresh==None or section_to_refresh==2:
		blocks[2]=get_array(int(minute/10) + add, parameters.section_widths[2])
	if section_to_refresh==None or section_to_refresh==3:
		blocks[3]=get_array(minute%10 + add, parameters.section_widths[3]) 
	return blocks	

def print_block(section, block):
	# the cursor should be at the top left location before and after that function
	block_left=0
#block_top is 0
	lines_down=0
	output="" # we clear the screen
	for i in range(0, section): # calculating space before top left of the block to print
		section_width=parameters.section_widths[i]
		block_left=block_left+section_width*parameters.led_width+(section_width*parameters.led_space)+parameters.block_vert_space
	s=""
	section_width=parameters.section_widths[section]
	for i in range(0, 3): # for each line
		for j in range(0, section_width):
			val=section_width*i+j
			if val in block:
				color=esc_colors[section]
			else:
				color=esc_empty_cell_color
			left=block_left+j*(parameters.led_width + parameters.led_space)
			output=output+color+"\033[%dG" % left
			output=output+"%s%s" % (color, block_str)
		output=output+"\n"
		lines_down=lines_down+1
		for i in range(0, parameters.block_horz_space):
			output=output+"\n"
			lines_down=lines_down+1 
	# we got to put the cursor n lines up now
	output=output+("\033[0m\033[%dF" % lines_down) 
	return output

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

