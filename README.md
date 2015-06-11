pluto
=====
The one and only Arduino framework in Python. It is built on top of [pyFirmata](https://github.com/tino/pyFirmata).

Intention
=========
+ A high-level Python interface to microcontrollers like the Arduinos.
+ Use asynchronous non-block I/O

Test status:

Untested (still in alpha).
Only tried on an Arduino Uno and Mac OSX 10.9.5.

Installation
============

```bash

git lcone https://github.com/jochasinga/pluto
cd pluto
python setup.py install

```

.. _setuptools: https://pypi.python.org/pypi/setuptools

Examples
========

Control on-board LED
--------------------

    >>> from pluto import *
    >>> board = Uno('/dev/cu.usbmodem1411')
    >>> board.led.on()
    >>> board.led.off()

*pluto* has `PortUtil` class which use *regex* to search for a relevant port.

    >>> PortUtil.scan()  # -> '/dev/cu.usbmodem1411'

This makes it possible to create an instance of the board without explicitly providing the port name.

    >>> board = Board()
    >>> board.led.blink()

`ArduinoUtil` is instantiated with the board so Arduino C-style APIs can be used.

    >>> board = Board()
    >>> board.digitalWrite(13, HIGH)
    >>> board.digitalWrite(13, LOW)

It's not Pythonic, and I'm considering replacing camelCase with underscore.

TODO
====

It's just a start, and there's a lot more to do. Here is a few ideas:

+ Implement PWM and analog functionalities.
+ Optimize the code and divide into several modules.
+ Make *pluto* a fork of *pyFirmata* instead of relying on it.











