#!/usr/bin/env python

import sys, os
import unittest
import serial
import pyfirmata
import re
import serial.tools.list_ports
from pyfirmata import mockup
from mock import Mock, patch

sys.path.append('./pluto')
import pluto
from boards import BOARDS
from utils import ArduinoUtil, PortUtil

class BoardBaseTest(unittest.TestCase):
    def setUp(self):
        pluto.serial.Serial = mockup.MockupSerial
        pluto.BOARD_SETUP_WAIT_TIME = 0
        self.board = pluto.Board()

    def tearDown(self):
        self.board.destroy()

class BoardInitTest(BoardBaseTest):
    def test_board_is_initiated(self):
        self.assertIsInstance(self.board, pluto.Board)

    def test_board_can_control_pin(self):
        self.assertIs(self.board.pin(13).high(), self.board.digital[13].write(1))
        self.assertIs(self.board.pin(13).low(), self.board.digital[13].write(0))

    def test_board_can_control_onboard_led(self):
        self.assertIs(self.board.led(13).on(), self.board.digital[13].write(1))
        self.assertIs(self.board.led(13).off(), self.board.digital[13].write(0))

    def test_board_can_control_arbitrary_led(self):
        self.assertIs(self.board.led(10).on(), self.board.digital[10].write(1))
        self.assertIs(self.board.led(10).off(), self.board.digital[10].write(0))

        # TODO: Test blink method
        # TODO: Test strope method

class PortUtilityTest(unittest.TestCase):

    def setUp(self):
        """Simulate PortUtil"""
        self.mock_portutil = Mock(spec=PortUtil)
        self.mock_portutil.num_ports = 3
        self.mock_portutil.auto_ports = '/dev/cu.usbmodem7321'
        self.mock_portutil.count_ports.return_value = self.mock_portutil.num_ports
        self.mock_portutil.scan.return_value = self.mock_portutil.auto_ports

    def test_auto_port_count(self):
        self.assertEqual(self.mock_portutil.count_ports(), self.mock_portutil.num_ports)

    def test_auto_port_discovery(self):
        self.assertEqual(self.mock_portutil.scan(), '/dev/cu.usbmodem7321')

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
