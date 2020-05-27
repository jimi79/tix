import datetime
import random
import shutil

class DisplaySettings:
    def __init__(self, style, use256, h24):
        self.led_width = 2
        self.led_space = 1
        self.block_horz_space = 1
        self.block_vert_space = 2
        self.section_widths = [1, 3, 2, 3] 
        if style == 2:
            self.section_widths=[4, 4, 4, 4]

        if use256:
            self.colors = [124, 34, 21, 124]
            self.esc_colors=["\033[48;5;%dm" % c for c in self.colors]
            self.esc_empty_cell_color="\033[48;5;233m"
        else:
            self.colors = [41, 42, 44, 41]
            self.esc_colors = ["\033[%dm" % c for c in self.colors]
            self.esc_empty_cell_color = "\033[40m"
        self.h24 = h24
        self.block_str = ""
        for i in range(0, self.led_width):
            self.block_str = self.block_str+" "


def get_center(display_settings):
    a = shutil.get_terminal_size()
    c = a.columns
    l = a.lines
    s = display_settings.section_widths
    w = sum(s) * (display_settings.led_width + display_settings.led_space) # the width of all leds
    w = w + len(s) * display_settings.block_vert_space # space between blocks
    h = 3 * (display_settings.block_horz_space + 1) # block size is globally fixed vertically
    X = int(c / 2 - w / 2)
    Y = int(l / 2 - h / 2)
    return {'X':X, 'Y' :Y}

def get_array(val, cols):
    c = [i for i in range(0,3*cols)]
    d = []
    for i in range(0,val):
        d.append(c.pop(random.randrange(len(c))))
    return d 

def get_cursor_pos_so_that_clock_is_centered():
    # return the position of the cursor
# i have to get the screen's size, maybe each time
    pass

def update(hour, minute, blocks, section_to_refresh, display_settings):
    # section_to_refresh was used when i thought i could just refresh one block, but it looks bad
    # i still keep it in case i change the behavior
    if blocks == None:
        blocks=[None, None, None, None]
    if section_to_refresh == None or section_to_refresh == 0:
        blocks[0] = get_array(int(hour/10), display_settings.section_widths[0])
    if section_to_refresh == None or section_to_refresh == 1:
        blocks[1] = get_array(hour%10, display_settings.section_widths[1])
    if section_to_refresh == None or section_to_refresh == 2:
        blocks[2] = get_array(int(minute/10), display_settings.section_widths[2])
    if section_to_refresh == None or section_to_refresh == 3:
        blocks[3] = get_array(minute%10, display_settings.section_widths[3]) 
    return blocks    

def print_block(section, block, X, Y, display_settings):
    output = "" # we clear the screen
    for i in range(0, section): # calculating space before top left of the block to print
        section_width = display_settings.section_widths[i]
        X = X + section_width * display_settings.led_width+(section_width*display_settings.led_space)+display_settings.block_vert_space
    output = "\033[%d;1H" % (Y+1) 

    count_added_lines = 0 # number of 
    section_width = display_settings.section_widths[section]
    for i in range(0, 3): # for each line
        for j in range(0, section_width):
            val = section_width*i+j
            if val in block:
                color = display_settings.esc_colors[section]
            else:
                color = display_settings.esc_empty_cell_color
            left = X+j*(display_settings.led_width + display_settings.led_space)
            output = output+color+"\033[%dG" % left
            output = output+"%s%s" % (color, display_settings.block_str)
        output = output+"\n"
        count_added_lines = count_added_lines+1
        for i in range(0, display_settings.block_horz_space):
            output = output+"\n"
            count_added_lines = count_added_lines+1 
    # we got to put the cursor n lines up now
    #output = output+("\033[%dF" % count_added_lines)  # might not be necessary, not sure though
    output = output+("\033[0m") 
    return output

def print_blocks(time, blocks, X, Y, display_settings): 
#def update(hour, minute, blocks, section_to_refresh, add):
    blocks = update(time[0], time[1], blocks, None, display_settings)
    s = "\033[2J"
    s = s+"\033[0;0H" # we put cursor top left, we'll change that later
    for i, block in zip(range(0, len(blocks)), blocks):
        s = s + print_block(i, block, X, Y, display_settings)
    return s

def get_time(old_time, format_):
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    if format_ == 12:
        hour = (hour - 1 ) % 12 + 1
    changed = []
    if old_time!=None:
        if old_time[0] !=  hour:
            changed.append(0)
        if old_time[1] !=  minute:
            changed.append(1)
    else:
        changed = [0, 1, 2 ,3]
    return [[hour, minute], changed]


def update_display(time, blocks, display_settings): 
    delay = random.randrange(0,10)/10+2.5 
    if display_settings.h24:
        format_ = 24
    else:
        format_ = 12
    time, changed = get_time(old_time = time, format_ = format_)
    center = get_center(display_settings)
    stdout = print_blocks(time, blocks, center['X'], center['Y'], display_settings)
    return time, blocks, stdout, delay 
    


