.. currentmodule:: esp32

:mod:`esp32` --- functionality specific to the ESP32
====================================================

.. autoapimodule:: esp32
    :no-members:
    :noindex:
    :platform: esp32



Functions
---------

.. autoapifunction:: wake_on_touch
    :noindex:    

.. autoapifunction:: wake_on_ulp
    :noindex:    

.. autoapifunction:: wake_on_ext0
    :noindex:    

.. autoapifunction:: wake_on_ext1
    :noindex:    

.. autoapifunction:: gpio_deep_sleep_hold
    :noindex:    

.. autoapifunction:: raw_temperature
    :noindex:    

.. autoapifunction:: idf_heap_info
    :noindex:    


    .. note:: Free IDF heap memory in the `esp32.HEAP_DATA` region is available
       to be automatically added to the MicroPython heap to prevent a
       MicroPython allocation from failing. However, the information returned
       here is otherwise *not* useful to troubleshoot Python allocation
       failures. :func:`micropython.mem_info()` and :func:`gc.mem_free()` should
       be used instead:

       The "max new split" value in :func:`micropython.mem_info()` output
       corresponds to the largest free block of ESP-IDF heap that could be
       automatically added on demand to the MicroPython heap.

       The result of :func:`gc.mem_free()` is the total of the current "free"
       and "max new split" values printed by :func:`micropython.mem_info()`.

Related constants
~~~~~~~~~~~~~~~~~

.. autoapidata:: HEAP_DATA
    :noindex:
.. autoapidata:: HEAP_EXEC
    :noindex:

    Used in `idf_heap_info`.


Flash partitions
----------------

This class gives access to the partitions in the device's flash memory and includes
methods to enable over-the-air (OTA) updates.

.. restore_section::

.. autoapiclass:: Partition
    :noindex:
    :members:
    :undoc-members:
    :private-members: 
    :special-members:


.. restore_section::




.. _esp32.RMT:

RMT
---

The RMT (Remote Control) module, specific to the ESP32, was originally designed
to send and receive infrared remote control signals. However, due to a flexible
design and very accurate (as low as 12.5ns) pulse generation, it can also be
used to transmit or receive many other types of digital signals::

    import esp32
    from machine import Pin

    r = esp32.RMT(0, pin=Pin(18), clock_div=8)
    r  # RMT(channel=0, pin=18, source_freq=80000000, clock_div=8, idle_level=0)

    # To apply a carrier frequency to the high output
    r = esp32.RMT(0, pin=Pin(18), clock_div=8, tx_carrier=(38000, 50, 1))

    # The channel resolution is 100ns (1/(source_freq/clock_div)).
    r.write_pulses((1, 20, 2, 40), 0)  # Send 0 for 100ns, 1 for 2000ns, 0 for 200ns, 1 for 4000ns

The input to the RMT module is an 80MHz clock (in the future it may be able to
configure the input clock but, for now, it's fixed). ``clock_div`` *divides*
the clock input which determines the resolution of the RMT channel. The
numbers specified in ``write_pulses`` are multiplied by the resolution to
define the pulses.

``clock_div`` is an 8-bit divider (0-255) and each pulse can be defined by
multiplying the resolution by a 15-bit (1-``PULSE_MAX``) number. There are eight
channels (0-7) and each can have a different clock divider.

So, in the example above, the 80MHz clock is divided by 8. Thus the
resolution is (1/(80Mhz/8)) 100ns. Since the ``start`` level is 0 and toggles
with each number, the bitstream is ``0101`` with durations of [100ns, 2000ns,
100ns, 4000ns].

For more details see Espressif's `ESP-IDF RMT documentation.
<https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/rmt.html>`_.

.. Warning::
   The current MicroPython RMT implementation lacks some features, most notably
   receiving pulses. RMT should be considered a
   *beta feature* and the interface may change in the future.


.. autoapiclass:: RMT
    :noindex:
    :members:
    :undoc-members:
    :private-members: 
    :special-members:    



Ultra-Low-Power co-processor
----------------------------

This class gives access to the Ultra Low Power (ULP) co-processor on the ESP32,
ESP32-S2 and ESP32-S3 chips.

.. warning::

    This class does not provide access to the RISCV ULP co-processor available
    on the ESP32-S2 and ESP32-S3 chips.

.. autoapiclass:: ULP()
    :noindex:
    :members:
    :undoc-members:
    :private-members: 
    :special-members:    


Related constants
~~~~~~~~~~~~~~~~~
.. restore_section::

.. autoapidata:: esp32.WAKEUP_ALL_LOW
   :noindex:

.. autoapidata:: esp32.WAKEUP_ANY_HIGH
   :noindex:

   Selects the wake level for pins.

Non-Volatile Storage
--------------------

This class gives access to the Non-Volatile storage managed by ESP-IDF. The NVS is partitioned
into namespaces and each namespace contains typed key-value pairs. The keys are strings and the
values may be various integer types, strings, and binary blobs. The driver currently only
supports 32-bit signed integers and blobs.

.. warning::

    Changes to NVS need to be committed to flash by calling the commit method. Failure
    to call commit results in changes being lost at the next reset.

.. autoapiclass:: NVS
    :noindex:
    :members:
    :undoc-members:
    :private-members: 
    :special-members:    
