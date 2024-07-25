:mod:`bluetooth` --- low-level Bluetooth
========================================

.. note:: For most applications, we recommend using the higher-level
          `aioble library <https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble>`_.

.. note:: This module is still under development and its classes, functions,
          methods and constants are subject to change.

.. autoapimodule:: bluetooth
    :no-index:
    :no-members:

Introduction
------------

This module provides the :class:`BLE` class which provides a BLE host stack
talking to a BLE controller (and radio) on the board. This will be typically
over an HCI UART (Pico W, Pyboard D) or built-in to the microcontroller (e.g.
esp32, stm32wb).

The BLE stack can be activated using :meth:`active<BLE.active>` and configured
using :meth:`config<BLE.config>`.

MicroPython can be built with either the `NimBLE <https://mynewt.apache.org/latest/network/>`_
(default on stm32, esp32) or `BlueKitchen <https://bluekitchen-gmbh.com/>`_ (default
on Pico W) host stacks. The functionality of both stacks is identical, with the
exception that l2cap channels and pairing & bonding is currently unsupported on
BlueKitchen.

A :class:`UUID` class is also provided for working with BLE service and
characteristic UUIDS.

Roles
-----

MicroPython supports the four BLE roles: Broadcaster, Observer, Central,
Peripheral. This functionality is available via the method starting with
``gap_``.

Broadcaster Role (Advertiser)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BLE advertisements can be sent using :meth:`gap_advertise<BLE.gap_advertise>`.
These include a payload (up to 31 bytes), and optionally a "scan response"
payload which will be send to active scanners.

Extended advertisements are currently not supported.

Observer Role (Scanner)
~~~~~~~~~~~~~~~~~~~~~~~

Both passive and active scanning is supported using the
:meth:`gap_scan<BLE.gap_scan>` method. Scan results are delivered asynchronously
via the ``_IRQ_SCAN_RESULT`` event.

Central Role
~~~~~~~~~~~~

A central device can connect to peripherals that it has discovered using the
observer role (see :meth:`gap_scan<BLE.gap_scan>`) or with a known address using
the :meth:`gap_connect<BLE.gap_connect>` method.

Typically a central will function as a GATT client, although it is also possible
to register services and function as a server.

When a central connects to a peripheral, the ``_IRQ_PERIPHERAL_CONNECT`` event
will be raised.

Peripheral Role
~~~~~~~~~~~~~~~

A peripheral device is expected to send connectable advertisements (see
:meth:`gap_advertise<BLE.gap_advertise>`).

Typically a peripheral will function as a GATT server by using
:meth:`gatts_register_services<BLE.gatts_register_services>`, although it is
also possible to act as a client and discover services on the central.

When a central connects, the ``_IRQ_CENTRAL_CONNECT`` event will be raised.

GATT
----

MicroPython supports implementing both GATT servers (using the ``gatts_``
methods) and clients (using the ``gattc_`` methods). A device can operate
as both a server and a client concurrently.

Devices in the central role may initiate an MTU exchange using
:meth:`gattc_exchange_mtu<BLE.gattc_exchange_mtu>`. Many other BLE
implementations do this automatically, but MicroPython does not, but you can
configure the default ``mtu`` that will be used in this exchange using
:meth:`BLE.config`.

GATT Server
~~~~~~~~~~~

A GATT server has a set of registered services. Each service may contain
characteristics, which each have a value. Characteristics can also contain
descriptors, which themselves have values.

These values are stored locally, and are accessed by their "value handle" which
is generated during service registration. They can also be read from or written
to by a remote client device. Additionally, a server can "notify" a
characteristic to a connected client via a connection handle.

A device in either central or peripheral roles may function as a GATT server,
however in most cases it will be more common for a peripheral device to act
as the server.

Characteristics and descriptors have a default maximum size of 20 bytes.
Anything written to them by a client will be truncated to this length. However,
any local write will increase the maximum size, so if you want to allow larger
writes from a client to a given characteristic, use
:meth:`gatts_write<BLE.gatts_write>` after registration. e.g.
``gatts_write(char_handle, bytes(100))``.

GATT Client
~~~~~~~~~~~

A GATT client can discover and read/write characteristics on a remote GATT server.

It is more common for a central role device to act as the GATT client, however
it's also possible for a peripheral to act as a client in order to discover
information about the central that has connected to it (e.g. to read the
device name from the device information service).

L2CAP connection-oriented-channels
----------------------------------

This feature allows for socket-like data exchange between two BLE devices.
Once the devices are connected via GAP, either device can listen for the
other to connect on a numeric PSM (Protocol/Service Multiplexer).

**Note:** This is currently only supported when using the NimBLE stack on
STM32 and Unix (not ESP32). Only one L2CAP channel may be active at a given
time (i.e. you cannot connect while listening).

Active L2CAP channels are identified by the connection handle that they were
established on and a CID (channel ID).

Connection-oriented channels have built-in credit-based flow control. Unlike
ATT, where devices negotiate a shared MTU, both the listening and connecting
devices each set an independent MTU which limits the maximum amount of
outstanding data that the remote device can send before it is fully consumed
in :meth:`l2cap_recvinto <BLE.l2cap_recvinto>`.

Pairing and bonding
-------------------

Pairing allows a connection to be encrypted and authenticated via exchange
of secrets (with optional MITM protection via passkey authentication).

Bonding is the process of storing those secrets into non-volatile storage.
When bonded, a device is able to resolve a resolvable private address (RPA)
from another device based on the stored identity resolving key (IRK).
To support bonding, an application must implement the ``_IRQ_GET_SECRET``
and ``_IRQ_SET_SECRET`` events.

**Note:** This is currently only supported when using the NimBLE stack on
STM32 and Unix (not ESP32).

Classes
-------

.. restore_section::

.. autoapiclass:: BLE
    :no-index:
    :members:
    :undoc-members:
    :private-members:    

.. autoapiclass:: UUID
    :no-index:
    :members:
    :undoc-members:
    :private-members:    