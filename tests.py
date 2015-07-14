#!/usr/bin/env python

import sys, os
import unittest2 as unittest
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
    """Base Class for generic boards"""    
    def setUp(self):
        pluto.serial.Serial = mockup.MockupSerial
        pluto.BOARD_SETUP_WAIT_TIME = 0
        self.board = pluto.Board()

    def tearDown(self):
        self.board.destroy()

class BoardUnoTest(BoardBaseTest):
    """Base Class for Arduino Uno"""
    def setUp(self):
        super(BoardUnoTest, self).setUp()
        self.board = pluto.Uno()

class BoardLilypadUSBTest(BoardBaseTest):
    """Base Class for Arduino LilypadUSB"""
    def setUp(self):
        super(BoardLilypadUSBTest, self).setUp()
        self.board = pluto.LilypadUSB()

class BoardInitTest(BoardBaseTest):
    """Test for generic board"""
    def test_board_is_initiated(self):
        self.assertIsInstance(self.board, pluto.Board)

    def test_board_name_defined(self):
        self.assertEqual(self.board.name, None)

    def test_board_can_control_pin(self):
        self.assertIs(self.board.pin(13).high(), self.board.digital[13].write(1))
        self.assertIs(self.board.pin(13).low(), self.board.digital[13].write(0))
        self.assertIs(self.board.pin(10).high(), self.board.digital[10].write(1))
        self.assertIs(self.board.pin(10).low(), self.board.digital[10].write(0))

    def test_board_remember_onboard_led(self):
        self.board.led(13).on()
        self.assertIs(self.board.led.off(), self.board.digital[13].write(0))
        self.assertIs(self.board.led.on(), self.board.digital[13].write(1))
        
    def test_board_can_control_onboard_led(self):
        self.assertIs(self.board.led(13).on(), self.board.digital[13].write(1))
        self.assertIs(self.board.led(13).off(), self.board.digital[13].write(0))

    def test_board_can_control_arbitrary_led(self):
        self.assertIs(self.board.led(10).on(), self.board.digital[10].write(1))
        self.assertIs(self.board.led(10).off(), self.board.digital[10].write(0))

        # TODO: Test blink method
        # TODO: Test strope method

class BoardUnoInitTest(BoardUnoTest, BoardInitTest):
    """Test for Uno"""
    def test_board_is_initiated(self):
        self.assertIsInstance(self.board, pluto.Uno)

    def test_board_name_defined(self):
        self.assertEqual(self.board.name, 'arduino')

class PortUtilityTest(unittest.TestCase):
    """Test for PortUtil methods"""
    def setUp(self):
        self.mock_portutil = Mock(spec=PortUtil)
        self.mock_portutil.num_ports = 3
        self.mock_portutil.auto_ports = '/dev/cu.usbmodem7321'
        self.mock_portutil.count_ports.return_value = self.mock_portutil.num_ports
        self.mock_portutil.scan.return_value = self.mock_portutil.auto_ports

    def test_auto_port_count(self):
        self.assertEqual(self.mock_portutil.count_ports(), self.mock_portutil.num_ports)

    def test_auto_port_discovery(self):
        self.assertEqual(self.mock_portutil.scan(), '/dev/cu.usbmodem7321')

class ArduinoUtilityTest(BoardBaseTest):
    """Test for ArduinoUtil methods"""
    def test_digital_write(self):
        self.assertIs(self.board.digitalWrite(13, 1), self.board.digital[13].write(1))

    def test_digital_read(self):
        self.assertIs(self.board.digitalRead(13), self.board.digital[13].read())

    def test_analog_write(self):
        self.assertIs(self.board.analogWrite(9, 0.5), self.board.digital[9].write(0.5))

class PinTest(unittest.TestCase):
    """Test for pins"""
    def setUp(self):
        self.board = pluto.Board()
        self.pin = pluto.Pin(self.board, 13)
        
    def test_pin_initiated(self):
        self.assertIsInstance(self.pin, pluto.Pin)

    def test_write_pin(self):
        self.assertIs(self.pin.high(), self.board.digital[13].write(1))
        self.assertIs(self.pin.low(), self.board.digital[13].write(0))
    
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
