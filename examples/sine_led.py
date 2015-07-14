'''
LED
Turns on and off (blink) an on-board LED with decremental intervals.

Pluto has collect some number of Arduino boards with on-board LED attached to pin 13. For these boards, Pluto can recognize automatically through the use of the board's class. If unsure, consult the doc at http://arduino.cc and use general Board class, then supply the pin number as the argument to led callable.

This example code is in the public domain.

modified June 22, 2015
by Joe Chasinga
'''

#!/usr/bin/env python

from __future__ import division
import sys, os, math
sys.path.append('../pluto')

from pluto import *
import time

board = Board()

def blink():
    angle = 0
    
    while True:
        t = abs(math.sin(angle))
        
        board.led(13).on()
        time.sleep(t/12)
        board.led(13).off()
        time.sleep(t/12)
        
        angle = angle + 0.02

if __name__ == '__main__':
    blink()
    
