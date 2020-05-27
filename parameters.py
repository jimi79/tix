led_width = 2
led_space = 1
block_horz_space = 1
block_vert_space = 2
style = 1 # refresh all blocks every 2.5 sec or so
#style = 2 # refresh one block every 0.5 sec and looping blocks 1-2-3-4
#style=3 # same as 2 but the count on each block is one more, so there is always one led on on each block
use_256_colors = True

section_widths = [1,3,2,3] # width for each section, in number of leds
if style == 3:
    section_widths=[1,4,3,4] # width for each section, in number of leds
