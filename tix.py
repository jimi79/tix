#!/usr/bin/python3

import signal
from tix_lib import *
from time import sleep
import random
import sys
import parameters
import argparse


def signal_handler(signal, frame):
    print("\033[?25h")
    #print("\033[%dE" % 3*(parameters.block_vert_space+1))
    sys.exit(0)

def run(h24):
    print("\033[?25l", end = "") # remove cursor
    signal.signal(signal.SIGINT, signal_handler)
    blocks=None
    time=None
    inc=0
    while True:
        time, blocks, stdout, delay=update_display(time, blocks, h24)
        print(stdout, end = "")
        sleep(delay)


parser = argparse.ArgumentParser(description = 'tix clock')
parser.add_argument('--24', action = 'store_const', const = True, default = False) 
args = parser.parse_args()
print(args)
run(h24 = args.__getattribute__('24'))
