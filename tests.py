#!/usr/bin/env python

import sys, os
import unittest
import serial
import pyfirmata
import re
import serial.tools.list_ports
from pyfirmata import mockup

sys.path.append('./pluto')
import pluto
from boards import BOARDS
from utils import ArduinoUtil, PortUtil

class BoardBaseTest(unittest.TestCase):
    def setUp(self):
        pluto.serial.Serial = mockup.MockupSerial
        pluto.BOARD_SETUP_WAIT_TIME = 0
        self.board = pluto.Board()

class BoardInitTest(BoardBaseTest):
    def test_board_initiated(self):
        self.assertIsInstance(self.board, pluto.Board)

    def test_board_led(self):
        self.assertEqual(self.board.led(13).on(), self.board.digital[13].write(1))
        self.assertEqual(self.board.led(13).off(), self.board.digital[13].write(0))
        self.assertEqual(self.board.led(10).on(), self.board.digital[10].write(1))
        self.assertEqual(self.board.led(10).off(), self.board.digital[10].write(0))
        
        # TODO: Test blink method
        # TODO: Test strope method

class PortUtilityTest(unittest.TestCase):
    def test_auto_port_count(self):
        self.comports = [p[0] for p in serial.tools.list_ports.comports()]
        self.assertEqual(PortUtil.count_ports(), len(self.comports))
    
    def test_auto_port_discovery(self):
        # TODO: Add new portnames to the list
        TEST_PORTS = [
            '/dev/cu.usbmodem1411',
            '/dev/tty.usbserial4321',
            '/dev/cu.usbbabe999',
            '/dev/tty.serialport666',
            '/dev/abc.usbrocks12'
        ]

        for port in TEST_PORTS:
            self.assertIn(PortUtil.scan(), TEST_PORTS)

class PinTest(BoardBaseTest):
    def test_pin_initiated(self):
        # TODO: Use MockPin
        self.pin = pluto.Pin(self.board)
        self.assertIsInstance(self.pin, pluto.Pin)

    def test_write_pin(self):
        pass
    
    def test_read_pin(self):
        pass
    
class TestBoardMessages(BoardBaseTest):
    def test_assert_serial(self, *incoming_bytes):
        serial_msg = bytearray()
        res = self.board.sp.read()
        while res:
            serial_msg += res
            res = self.board.sp.read()
        self.assertEqual(bytearray(incoming_bytes), serial_msg)
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
