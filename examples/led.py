'''
LED
Turns on and off an on-board LED 

Pluto has collect some number of Arduino boards with on-board LED attached to pin 13. For these boards, Pluto can recognize automatically through the use of the board's class. If unsure, consult the doc at http://arduino.cc and use general Board class, then supply the pin number as the argument to led callable.

This example code is in the public domain.

modified June 22, 2015
by Joe Chasinga
'''

#!/usr/bin/env python

import sys, os
sys.path.append('../pluto')

from pluto import *
import time

def main():
    board = Board()
    board.led(13).on()
    time.sleep(5)
    board.led(13).off()

if __name__ == '__main__':
    main()
    
