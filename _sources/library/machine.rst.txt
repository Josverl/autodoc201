:mod:`machine` --- functions related to the hardware
====================================================

.. autoapimodule:: machine
   :synopsis: functions related to the hardware

The ``machine`` module contains specific functions related to the hardware
on a particular board. Most functions in this module allow to achieve direct
and unrestricted access to and control of hardware blocks on a system
(like CPU, timers, buses, etc.). Used incorrectly, this can lead to
malfunction, lockups, crashes of your board, and in extreme cases, hardware
damage.

.. _machine_callbacks:

A note of callbacks used by functions and class methods of :mod:`machine` module:
all these callbacks should be considered as executing in an interrupt context.
This is true for both physical devices with IDs >= 0 and "virtual" devices
with negative IDs like -1 (these "virtual" devices are still thin shims on
top of real hardware and real hardware interrupts). See :ref:`isr_rules`.

Memory access
-------------

The module exposes three objects used for raw memory access.

.. autoapidata:: mem8
.. autoapidata:: mem16
.. autoapidata:: mem32

Use subscript notation ``[...]`` to index these objects with the address of
interest. Note that the address is the byte address, regardless of the size of
memory being accessed.

Example use (registers are specific to an stm32 microcontroller):

.. code-block:: python3

    import machine
    from micropython import const

    GPIOA = const(0x48000000)
    GPIO_BSRR = const(0x18)
    GPIO_IDR = const(0x10)

    # set PA2 high
    machine.mem32[GPIOA + GPIO_BSRR] = 1 << 2

    # read PA3
    value = (machine.mem32[GPIOA + GPIO_IDR] >> 3) & 1

Reset related functions
-----------------------

.. autoapifunction:: reset
.. autoapifunction:: soft_reset
.. autoapifunction:: reset_cause
.. autoapifunction:: bootloader

Interrupt related functions
---------------------------

The following functions allow control over interrupts.  Some systems require
interrupts to operate correctly so disabling them for long periods may
compromise core functionality, for example watchdog timers may trigger
unexpectedly.  Interrupts should only be disabled for a minimum amount of time
and then re-enabled to their previous state.  For example::

    import machine

    # Disable interrupts
    state = machine.disable_irq()

    # Do a small amount of time-critical work here

    # Enable interrupts
    machine.enable_irq(state)


.. autoapifunction:: disable_irq
.. autoapifunction:: enable_irq

Power related functions
-----------------------

.. autoapifunction:: freq
.. autoapifunction:: idle
.. autoapifunction:: sleep
.. autoapifunction:: lightsleep
.. autoapifunction:: deepsleep
.. autoapifunction:: wake_reason

Miscellaneous functions
-----------------------

.. autoapifunction:: unique_id
.. autoapifunction:: time_pulse_us
.. autoapifunction:: bitstream
.. autoapifunction:: rng


.. _machine_constants:

Constants
---------

.. autoapidata:: machine.IDLE
.. autoapidata:: machine.SLEEP
.. autoapidata:: machine.DEEPSLEEP

.. autoapidata:: machine.PWRON_RESET
.. autoapidata:: machine.HARD_RESET
.. autoapidata:: machine.WDT_RESET
.. autoapidata:: machine.DEEPSLEEP_RESET
.. autoapidata:: machine.SOFT_RESET

.. autoapidata:: machine.WLAN_WAKE
.. autoapidata:: machine.PIN_WAKE
.. autoapidata:: machine.RTC_WAKE


Classes
-------

.. toctree::
   :maxdepth: 1

   machine.Pin.rst
   machine.Signal.rst
   machine.ADC.rst
   machine.ADCBlock.rst
   machine.PWM.rst
   machine.UART.rst
   machine.SPI.rst
   machine.I2C.rst
   machine.I2S.rst
   machine.RTC.rst
   machine.Timer.rst
   machine.WDT.rst
   machine.SD.rst
   machine.SDCard.rst
   machine.USBDevice.rst
