pluto
=====
The Python Arduino framework built on top of [pyFirmata](https://github.com/tino/pyFirmata).

Intention
=========
A high-level Python interface to control Arduino boards for easy prototyping.
Compatible with Python >= 2.6 and 3.x.


Test status:

![build-status](https://travis-ci.org/jochasinga/pluto.svg?branch=master)

Installation
============

```bash

git clone https://github.com/jochasinga/pluto
cd pluto
python setup.py install

```
setuptools: [https://pypi.python.org/pypi/setuptools](https://pypi.python.org/pypi/setuptools)

It is currently not on Pypi, so `pip` installation is not available yet.

Upload Firmata
==============
+ Fire up Arduino software
+ Choose the appropriate board and port name
+ Go to File > Examples > Firmata > StandardFirmata
+ Click upload

Download the Arduino software here: [http://www.arduino.cc/en/Main/Software](http://www.arduino.cc/en/Main/Software)

Examples
========

All code snippets here are using Python interactive shell. To use it, open the terminal app and on the command line type `python` to enter the `>>>` interpreter mode.

Creating a Board
----------------
    >>> from pluto import *                   # import everything
    >>> board = Uno('/dev/cu.usbmodem1411')   # for Arduino Uno

*note*: `from <package> import *` is not necessary and not a good idea if you will be doing any development, but for simple usage it imports convenient constants like `LOW`, `HIGH`, and `LED_BUILTIN`.

**pluto** has `PortUtil` class which use **regex** to search for a relevant port.

    >>> PortUtil.scan()  # -> '/dev/cu.usbmodem1411'

Every board instance has a `PortUtil` object created. This makes it possible to create an instance of any board without explicitly providing the port name.

    >>> board = Board()        # Create a generic board
    >>> my_lily = LilypadUSB() # Create a Lilypad USB board

Control an LED
--------------

Controlling an on-board LED is very easy.

    >>> board.led.on()
    >>> board.led.off()
    >>> board.led.blink()

However, to control an on-board LED on a "generic" board created by the `Board` class, you should provide a pin number of the on-board LED **for the first time**:

    >>> board.led(9).on() # This board has a built-in LED on pin 9
    >>> board.led.on()    # The pin number is injected into `led` attribute.

To control an LED connected to an arbitrary pin:

    >>> board.led(pin_number).on()

Note that the `led` attribute of the board does not change to that latest pin number but stay as the on-board LED.

You can also create Led instances separately

    >>> led = Led(board)      # This creates Led instance at pin 13
    >>> led.on()
    >>> led.off()
    >>> led_1 = Led(board, 9) # Led instance at pin 9
    >>> led_1.strobe()

Control a Pin
-------------

In Pluto, `Led` inherits from `Pin`, therefore you can do more basic things like writing and reading from a pin.

    >>> pin = Pin(board, 10)  # Initiate a `Pin` instance at pin 10
    >>> pin.high()            # Guess what this does!
    >>> pin.low()
    >>> pin.pulse()           # Use PWM just like Led's strobe.

Just like `Led` you can control pins as the board's attribute.

    >>> board = Board()
    >>> board.pin(10).high()

Arduino-style APIs
------------------

`ArduinoUtil` instance is instantiated with the board to allow Arduino C-style APIs for arduino users.

    >>> board = Board()
    >>> board.digitalWrite(13, HIGH)
    >>> board.digitalWrite(13, LOW)
    >>> board.analogWrite(9, 0.5)
    >>> my_val = board.pin(13).digitalRead()

It's not Pythonic, with camelCase methods but it's a set of APIs for Arduino users. Maybe will consider using under_score.

Run code in *examples/* to find out more.

TODO
====

It's just a start, and there's a lot more to do. Here is a few ideas:

+ Implement PWM. (ONGOING)
+ Implement digitalRead and analogRead.
+ Optimize the code and divide into several modules.
+ Make *pluto* a fork of *pyFirmata* instead of relying on the library.











