.. currentmodule:: machine
.. _machine.Pin:

class Pin -- control I/O pins
=============================

A pin object is used to control I/O pins (also known as GPIO - general-purpose
input/output).  Pin objects are commonly associated with a physical pin that can
drive an output voltage and read input voltages.  The pin class has methods to set the mode of
the pin (IN, OUT, etc) and methods to get and set the digital logic level.
For analog control of a pin, see the :class:`ADC` class.

A pin object is constructed by using an identifier which unambiguously
specifies a certain I/O pin.  The allowed forms of the identifier and the
physical pin that the identifier maps to are port-specific.  Possibilities
for the identifier are an integer, a string or a tuple with port and pin
number.

Usage Model::

    from machine import Pin

    # create an output pin on pin #0
    p0 = Pin(0, Pin.OUT)

    # set the value low then high
    p0.value(0)
    p0.value(1)

    # create an input pin on pin #2, with a pull up resistor
    p2 = Pin(2, Pin.IN, Pin.PULL_UP)

    # read and print the pin value
    print(p2.value())

    # reconfigure pin #0 in input mode with a pull down resistor
    p0.init(p0.IN, p0.PULL_DOWN)

    # configure an irq callback
    p0.irq(lambda p:print(p))

.. autoapiclass:: machine.Pin
    :members:
    :undoc-members:
    :inherited-members:
    :private-members:
    :special-members:
    :no-index: