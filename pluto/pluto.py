from pyfirmata import *
from boards import BOARDS
from ports import *
import gevent

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
    def digitalWrite(board, pin_number, value):
        if isinstance(board, Board):
            board.digital[pin_number].write(value)

    @staticmethod
    def digitalRead(board, pin_number, value):
        if isinstance(board, Board):
            board.digital[pin_number].read()

    @staticmethod
    def blinkLED(board, pin_number=LED_BUILTIN, interval=1):
        if isinstance(board, Board):
            while True:
                board.digital[pin_number].write(HIGH)
                gevent.sleep(1)
                board.digital[pin_number].write(LOW)
                gevent.sleep(1)

class Board(pyfirmata.Board):
    """The Base class for any board."""
    def __init__(self, port=None, layout=None, baudrate=57600, name=None, timeout=None):
        self.util = ArduinoUtil()
        self.led = Led(self)
        self.pin = Pin(self)
        auto_port = PortUtil.scan()
        self.sp = serial.Serial(auto_port, baudrate, timeout=timeout)
        # Allow 5 secs for Arduino's auto-reset to happen
        # Alas, Firmata blinks its version before printing it to serial
        # For 2.3, even 5 seconds might not be enough.
        # TODO Find a more reliable way to wait until the board is ready
        self.pass_time(BOARD_SETUP_WAIT_TIME)
        self.name = name
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

    def blinkLED(self, pin_number=13, interval=1):
        self.util.blinkLED(self)

    def at_pin(self, pin_number):
        self.pin = Pin(self, pin_number)
                
class Pin(pyfirmata.Pin):
    """Pluto's Pin representation"""
    def __init__(self, board, pin_number=LED_BUILTIN, type=ANALOG, port=None):
        super(Pin, self).__init__(board, pin_number, type, port)
        self.util = ArduinoUtil()
        
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

    def high(self):
        self.digitalWrite(pin_number=self.pin_number, value=HIGH)

    def low(self):
        self.digitalWrite(pin_number=self.pin_number, value=LOW)
                
class Led(Pin):
    """Led representation"""    
    def __init__(self, board, pin_number=LED_BUILTIN, type=ANALOG, port=None):
        super(Led, self).__init__(board, pin_number, type, port)

    def on(self):
        self.board.digitalWrite(self.pin_number, HIGH)
    
    def off(self):
        self.board.digitalWrite(self.pin_number, LOW)

    def blink(self, interval=1, forever=True):
        if forever:
            while True:
                self.board.digitalWrite(self.pin_number, HIGH)
                gevent.sleep(interval)
                self.board.digitalWrite(self.pin_number, LOW)
                gevent.sleep(interval)

class Uno(Board):
    """
    A board that will set itself up as an Arduino Uno
    """
    def __init__(self, *args, **kwargs):
        super(Uno, self).__init__(*args, **kwargs)
        self.name = 'arduino_uno'

    def __str__(self):
        super(Uno, self).__str__()

class Mega(Board):
    """
    A board that will set itself up as an ArduinoMega
    """
    def __init__(self, *args, **kwargs):
        super(Mega, self).__init__(*args, **kwargs)
        self.util = ArduinoUtil()
        self.led = Led(self)

    def __str__(self):
        super(Mega, self).__str__()

class SparkCore(Board):
    """
    A board that will set itself up as a Spark Core
    """
    def __init__(self, *args, **kwargs):
        super(SparkCore, self).__init__(*args, **kwargs)
        self.util = ArduinoUtil()
        self.led = Led(self)

class Lilypad(Board):
    """
    A board that will set itself up as an ArduinoLilypad
    """
    def __init__(self, *args, **kwargs):
        args = list(args)
        args.append(BOARDS['arduino_lilypad'])
        super(Lilypad, self).__init__(*args, **kwargs)
        self.name = 'arduino_lilypad'
        self.util = ArduinoUtil()
        self.led = Led(self)

        
        
        

    
    

    
