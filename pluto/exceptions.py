#!/usr/env/bin python

"""Custom exceptions for Pluto"""

class PinError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
