pluto
=====
The Python Arduino framework built on top of [pyFirmata](https://github.com/tino/pyFirmata).

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

git clone https://github.com/jochasinga/pluto
cd pluto
python setup.py install

```
setuptools: https://pypi.python.org/pypi/setuptools

It is currently not only Pypi, so `pip` installation is not available (yet). 

Examples
========

Control on-board LED
--------------------

    >>> from pluto *
    >>> board = Uno('/dev/cu.usbmodem1411')
    >>> board.led.on()
    >>> board.led.off()

**pluto** has `PortUtil` class which use **regex** to search for a relevant port.

    >>> PortUtil.scan()  # -> '/dev/cu.usbmodem1411'

This makes it possible to create an instance of the board without explicitly providing the port name.

    >>> board = Board()

However, to control an on-board LED on an anonymous board, you should provide an a pin number for the first time:

    >>> board.led(9).on() # This board has a built-in LED on pin 9
    >>> board.led.off()   # After that it is not necessary anymore
    

One can also create Led instances

    >>> led = Led(board)
    >>> led.on()
    >>> led.off()

`ArduinoUtil` is instantiated with the board so Arduino C-style APIs can be used.

    >>> board = Board()
    >>> board.digitalWrite(13, HIGH)
    >>> board.digitalWrite(13, LOW)

It's not Pythonic, and I'm considering replacing camelCase with under_score.

TODO
====

It's just a start, and there's a lot more to do. Here is a few ideas:

+ Implement PWM and analog functionalities.
+ Optimize the code and divide into several modules.
+ Make *pluto* a fork of *pyFirmata* instead of relying on the library.











