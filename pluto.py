from pyfirmata import *
from boards import BOARDS
import time

__version__ = '0.1.0'

# convenient contants
LOW = 0
HIGH = 1
LED_BUILTIN = 13

class ArduinoUtil(object):
    """
    A utility class containing all the Arduino-esque functions
    """
    @staticmethod
    def digitalWrite(board, pin, value):
        if isinstance(board, Board):
            board.digital[pin].write(value)

    @staticmethod
    def digitalRead(board, pin, value):
        if isinstance(board, Board):
            board.digital[pin].read()

    @staticmethod
    def blinkLED(board, pin=13, interval=1):
        if isinstance(board, Board):
            while True:
                board.digital[pin].write(HIGH)
                time.sleep(1)
                board.digital[pin].write(LOW)
                time.sleep(1)

# wrapper classes
class Uno(Board):
    """
    A board that will set itself up as an Arduino Uno
    """
    def __init__(self, *args, **kwargs):
        super(Uno, self).__init__(*args, **kwargs)
        self.util = ArduinoUtil()
        self.led = Led()

    def digitalWrite(self, pin, value):
        self.util.digitalWrite(self, pin, value)

    def digitalRead(self):
        self.util.digitalRead(self)

    def blinkLED(self, pin=13, interval=1):
        self.util.blinkLED(self)

    def __str__(self):
        super(Uno, self).__str__()

class Mega(Board):
    """
    A board that will set itself up as an ArduinoMega
    """
    def __init__(self, *args, **kwargs):
        super(Mega, self).__init__(*args, **kwargs)

    def __str__(self):
        super(Mega, self).__str__()

class SparkCore(Board):
    """
    A board that will set itself up as a Spark Core
    """
    def __init__(self, *args, **kwargs):
        super(SparkCore, self).__init__(*args, **kwargs)

class Lilypad(Board):
    """
    A board that will set itself up as an ArduinoLilypad
    """
    def __init__(self, *args, **kwargs):
        args = list(args)
        args.append(BOARDS['arduino_lilypad'])
        super(Lilypad, self).__init__(*args, **kwargs)
        self.name = 'arduino_lilypad'

        
        
        

    
    

    
