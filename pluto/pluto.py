from __future__ import print_function

from pyfirmata import *
from boards import BOARDS
import time

__version__ = '0.1.0'

# convenient contants
LOW = 0
HIGH = 1
LED_BUILTIN = 13

from utils import ArduinoUtil, PortUtil

class Board(pyfirmata.Board):
    """The Base class for any board."""
    # TODO: auto-scan for type of board
    def __init__(self, port=None, layout=BOARDS['arduino'], baudrate=57600, name=None, timeout=None):
        """
        default_leds = [
            'arduino',
            'arduino_leonardo',
            'arduino_mega',
            'arduino_due',
            'arduino_yun',
            'arduino_zero',
            'arduino_micro',
            'arduino_lilypad_usb',
        ]
        """
        # Arduino boards with on-board digital LED @ pin 13
        default_leds = [
            'Uno',
            'LilypadUSB',
        ]

        def led_hook(pin_number):
            led = Led(self, pin_number)
            self.led = led
            return led

        def pin_hook(pin_number):
            pin = Pin(self, pin_number)
            self.pin = pin
            return pin
        
        self.name = name
        self.util = ArduinoUtil()
        self.pin = (lambda pin_number: pin_hook(pin_number))
        #self.led = Led(self) if self.name in default_leds else (lambda pin_number: led_hook(pin_number))
        # Use class's name instead of name attribute
        self.led = Led(self) if self.__class__.__name__ in default_leds else (lambda pin_number: led_hook(pin_number))
        auto_port = PortUtil.scan()
        self.sp = serial.Serial(auto_port, baudrate, timeout=timeout)
        # Allow 5 secs for Arduino's auto-reset to happen
        # Alas, Firmata blinks its version before printing it to serial
        # For 2.3, even 5 seconds might not be enough.
        # TODO Find a more reliable way to wait until the board is ready
        self.pass_time(BOARD_SETUP_WAIT_TIME)
        self._layout = layout
        if not self.name:
            self.name = port

        if layout:
            self.setup_layout(layout)
        else:
            self.auto_setup()

        # Iterate over the first messages to get firmware data
        while self.bytes_available():
            self.iterate()
        # TODO Test whether we got a firmware name and version, otherwise there
        # probably isn't any Firmata installed

    def digitalWrite(self, pin_number, value):
        self.util.digitalWrite(self, pin_number, value)

    def digitalRead(self):
        self.util.digitalRead(self)

    def analogWrite(self, pin_number, value):
        self.util.analogWrite(self, pin_number, value)

    def blinkLED(self, pin_number=13, interval=1):
        self.util.blinkLED(self)

    def at_pin(self, pin_number):
        self.pin = Pin(self, pin_number)

    def destroy(self):
        super(Board, self).exit()

class Pin(pyfirmata.Pin):
    """Pluto's Pin representation"""    
    def __init__(self, board, pin_number=LED_BUILTIN, type=ANALOG, port=None):
        super(Pin, self).__init__(board, pin_number, type, port)
        self.util = ArduinoUtil()

    def __call__(self, pin_number):
        return Pin(self.board, pin_number)
        
    def digitalWrite(self, *args, **kwargs):
        for index, val in enumerate(args):
            if index == 0:
                self.pin_number = val
            elif index == 1:
                self.value = val

        if kwargs is not None:
            for key, val in kwargs.iteritems():
                if key == "pin_number":
                    self.pin_number = val
                elif key == "value":
                    self.value = val
                else:
                    pass

        self.util.digitalWrite(self.board, self.pin_number, self.value)

    def analogWrite(self, *args, **kwargs):
        for index, val in enumerate(args):
            if index == 0:
                self.pin_number = val
            elif index == 1:
                self.value = val

        if kwargs is not None:
            for key, val in kwargs.iteritems():
                if key == "pin_number":
                    self.pin_number = val
                elif key == "value":
                    self.value = val
                else:
                    pass

        self.util.analogWrite(self.board, self.pin_number, self.value)

    def high(self):
        self.digitalWrite(pin_number=self.pin_number, value=HIGH)

    def low(self):
        self.digitalWrite(pin_number=self.pin_number, value=LOW)

    def alternate(self, interval=1, forever=True):
        while forever:
            self.digitalWrite(pin_number=self.pin_number, value=HIGH)
            time.sleep(interval)
            self.digitalWrite(pin_number=self.pin_number, value=LOW)
            time.sleep(interval)

    def pulse(self, step=1, forever=True):
        val = 0
        while forever:
            if val <= 10000:
                val = val + step
            else:
                val = val - step
                
            self.analogWrite(pin_number=self.pin_number, value=val/10000)
                
class Led(Pin):
    """Led representation"""
    def __init__(self, board, pin_number=LED_BUILTIN, type=ANALOG, port=None):
        super(Led, self).__init__(board, pin_number, type, port)
        self.blinking = False

    def __call__(self, pin_number):
        return Led(self.board, pin_number)

    def on(self):
        self.board.digitalWrite(self.pin_number, HIGH)
    
    def off(self):
        self.board.digitalWrite(self.pin_number, LOW)

    def blink(self, interval=1, forever=True):
        super(Led, self).alternate(interval, forever)
        self.blinking = True

    def strobe(self, step=1, forever=True):
        super(Led, self).pulse(step, forever)
        self.strobing = True

class Uno(Board):
    """
    A board that will set itself up as an Arduino Uno
    """
    def __init__(self, *args, **kwargs):
        super(Uno, self).__init__(*args, **kwargs)
        self.name = 'arduino'

    def __str__(self):
        super(Uno, self).__str__()

class Mega(Board):
    """
    A board that will set itself up as an ArduinoMega
    """
    def __init__(self, *args, **kwargs):
        args = list(args)
        args.append(BOARDS['arduino_mega'])
        super(Mega, self).__init__(*args, **kwargs)

    def __str__(self):
        super(Mega, self).__str__()
        
#TODO: Look at Serial conflict for Yun
'''
class Yun(Board):
    """
    A board that will set itself up as an ArduinoYun
    """
    def __init__(self, *args, **kwargs):
        args = list(args)
        args.append(BOARDS['arduino_yun'])
        super(Yun, self).__init__(*args, **kwargs)
'''

class SparkCore(Board):
    """
    A board that will set itself up as a Spark Core
    """
    def __init__(self, *args, **kwargs):
        super(SparkCore, self).__init__(*args, **kwargs)

class LilypadUSB(Board):
    """
    A board that will set itself up as an ArduinoLilypadUSB
    """
    def __init__(self, *args, **kwargs):
        args = list(args)
        args.append(BOARDS['arduino_lilypad_usb'])
        super(LilypadUSB, self).__init__(*args, **kwargs)
        self.name = 'arduino_lilypad_usb'


        
        
        

    
    

    
