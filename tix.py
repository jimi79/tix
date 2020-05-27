#!/usr/bin/python3

import signal
from tix_lib import *
from time import sleep
import random
import sys
import argparse


def signal_handler(signal, frame):
    print("\033[?25h")
    #print("\033[%dE" % 3*(parameters.block_vert_space+1))
    sys.exit(0)

def run(h24, style, no256):
    print("\033[?25l", end = "") # remove cursor
    signal.signal(signal.SIGINT, signal_handler)
    blocks = None
    time = None
    inc = 0
    display_settings = DisplaySettings(use256 = not no256, style = style, h24 = h24)
    while True:
        time, blocks, stdout, delay = update_display(time, blocks, display_settings)
        print(stdout, end = "")
        sleep(delay)


parser = argparse.ArgumentParser(description = 'tix clock')
parser.add_argument('--24', help = 'use a 24h format time', action = 'store_true', default = False) 
parser.add_argument('--style', help = 'style 1 or 2', default = 1, type = int) 
parser.add_argument('--no256', help = 'do not use 256 colors', action = 'store_true', default = False) 

args = parser.parse_args()
print(args)
run(h24 = args.__getattribute__('24'), no256 = args.no256, style = args.style)
