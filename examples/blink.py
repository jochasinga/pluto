'''
Blink
Turns on an on-board LED on for one second, then off for one second repeatedly.

Most Arduinos have an on-board LED you can control. On the Uno and Leonardo,
it is attached to digital pin 13. If you're unsure what pin the on-board LED
is connected to on your Arduino model, check the doc at http://arduino.cc

This example code is in the public domain.

modified June 13, 2015
by Joe Chasinga
'''

#!/usr/bin/env python

import sys, os
sys.path.append('../pluto')

from pluto import *
import time

def main():
    # Invoke a general board
    board = Board()
    board.led(13).blink()

if __name__ == '__main__':
    main()
    
