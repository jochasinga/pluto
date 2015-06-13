#!/usr/bin/env python

import sys, os
import unittest
import serial
import pyfirmata
from pyfirmata import mockup

sys.path.append('./pluto')
import pluto
from boards import BOARDS
from utils import ArduinoUtil, PortUtil

TEST_PORT = '/dev/cu.usbmodem1411'

class BoardBaseTest(unittest.TestCase):
    def setUp(self):
        pluto.serial.Serial = mockup.MockupSerial
        pluto.BOARD_SETUP_WAIT_TIME = 0
        self.board = pluto.Board()

class BoardInitTest(BoardBaseTest):
    def test_board_initiated(self):
        self.assertIsInstance(self.board, pluto.Board)

class UtilityTest(unittest.TestCase):
    def test_auto_port_count(self):
        self.assertIsNotNone(PortUtil.count_ports())
    
    def test_auto_port_discovery(self):
        self.assertEqual(PortUtil.scan(), TEST_PORT)

    def test_arduino_utility(self):
        # self.util.digitalWrite(self.board, 13, HIGH)
        pass

class PinTest(BoardBaseTest):
    def test_pin_initiated(self):
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
