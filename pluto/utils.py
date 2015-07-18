from builtins import object
import pluto
import re
import serial.tools.list_ports
import time
from pyfirmata import util, OUTPUT, INPUT, PWM
from pluto import LOW, HIGH, LED_BUILTIN
import exceptions

class ArduinoUtil(object):
    """
    A utility class containing all the Arduino-esque functions
    """
    @staticmethod
    def digitalWrite(board, pin_number, value):
        if isinstance(board, pluto.Board):
            if board.digital[pin_number].mode != OUTPUT:
                board.digital[pin_number].mode = OUTPUT
            else:
                pass
            board.digital[pin_number].write(value)
        else:
            raise TypeError("The object isn't an instance of 'pluto.Board'")

    @staticmethod
    def digitalRead(board, pin_number):
        if isinstance(board, pluto.Board):
            if board.digital[pin_number].mode != INPUT:
                board.digital[pin_number].mode = INPUT
            else:
                pass
            board.digital[pin_number].read()
        else:
            raise TypeError("The object isn't an instance of 'pluto.Board'.")

    @staticmethod
    def analogWrite(board, pin_number, value):
        if isinstance(board, pluto.Board):
            if board.digital[pin_number].PWM_CAPABLE:
                if board.digital[pin_number].mode != 3:
                    board.digital[pin_number]._set_mode(PWM)
                else:
                    pass
                board.digital[pin_number].write(value)
            else:
                raise exceptions.PinError("This pin is not PWM capable.")
        else:
            raise TypeError("The object isn't an instance of 'pluto.Board'.")

    @staticmethod
    def analogRead(board, pin_number):
        if isinstance(board, pluto.Board):
            board.analog[pin_number].read()
        else:
            raise TypeError("The object isn't an instance of 'pluto.Board'.")

class PortUtil(object):
    """Helper class that scan serial port automatically"""
    comports = [p[0] for p in serial.tools.list_ports.comports()]
    num_ports = len(comports)
    auto_port = None
    keywords = []
    patterns = []

    @classmethod
    def count_ports(cls):
        return cls.num_ports

    @classmethod
    def scan(cls, *args, **kwargs):
        if len(args) == 0:
            cls.keywords = ['usb', 'serial']
        else:
            for index, val in enumerate(args):
                cls.keywords.append(val)

        for keyword in cls.keywords:
            p = re.compile('(/dev/)((tty)|(cu)|.*).({0})\w*[\d]'.format(keyword))
            cls.patterns.append(p)

        for port in cls.comports:
            for pattern in cls.patterns:
                m = pattern.match(port)
                if m:
                    cls.auto_port = m.group()
                else:
                    pass

        return cls.auto_port
