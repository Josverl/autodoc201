:mod:`bluetooth` --- low-level Bluetooth
========================================

.. autoapimodule:: bluetooth
    :no-index:
    :no-members:

Classes
-------

.. autoapisummary::

   bluetooth.BLE
   bluetooth.UUID


class BLE
---------

.. autoapiclass:: BLE
    :no-index:
    :members: active, config

Event Handling
--------------

.. autoapimethod:: BLE.irq
    :no-index:

Broadcaster Role (Advertiser)
-----------------------------

.. autoapimethod:: BLE.gap_advertise
    :no-index:

Observer Role (Scanner)
-----------------------

.. autoapimethod:: BLE.gap_scan
    :no-index:


Central Role
------------

A central device can connect to peripherals that it has discovered using the observer role 
(see :meth:`gap_scan<BLE.gap_scan>`) or with a known address.

.. autoapimethod:: BLE.gap_connect
    :no-index:

Peripheral Role
---------------

A peripheral device is expected to send connectable advertisements (see
:meth:`gap_advertise<BLE.gap_advertise>`). It will usually be acting as a GATT
server, having first registered services and characteristics using
:meth:`gatts_register_services<BLE.gatts_register_services>`.

When a central connects, the ``_IRQ_CENTRAL_CONNECT`` event will be raised.

Central & Peripheral Roles
--------------------------

.. autoapimethod:: BLE.gap_disconnect
    :no-index:

GATT Server
-----------

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

.. autoapimethod:: BLE.gatts_register_services
    :no-index:

.. autoapimethod:: BLE.gatts_read
    :no-index:

.. autoapimethod:: BLE.gatts_write
    :no-index:

.. autoapimethod:: BLE.gatts_notify
    :no-index:

.. autoapimethod:: BLE.gatts_indicate
    :no-index:

.. autoapimethod:: BLE.gatts_set_buffer
    :no-index:

GATT Client
-----------

A GATT client can discover and read/write characteristics on a remote GATT server.

It is more common for a central role device to act as the GATT client, however
it's also possible for a peripheral to act as a client in order to discover
information about the central that has connected to it (e.g. to read the
device name from the device information service).

.. autoapimethod:: BLE.gattc_discover_services
    :no-index:

.. autoapimethod:: BLE.gattc_discover_characteristics
    :no-index:

.. autoapimethod:: BLE.gattc_discover_descriptors
    :no-index:

.. autoapimethod:: BLE.gattc_read
    :no-index:

.. autoapimethod:: BLE.gattc_write
    :no-index:

.. autoapimethod:: BLE.gattc_exchange_mtu
    :no-index:

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

.. autoapimethod:: BLE.l2cap_listen   
    :no-index:

.. autoapimethod:: BLE.l2cap_connect
    :no-index:

.. autoapimethod:: BLE.l2cap_disconnect
    :no-index:

.. autoapimethod:: BLE.l2cap_send
    :no-index:

.. autoapimethod:: BLE.l2cap_recvinto
    :no-index:


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
    ESP32, STM32 and Unix.

.. autoapimethod:: BLE.gap_pair
    :no-index:

.. autoapimethod:: BLE.gap_passkey
    :no-index:

class UUID
----------

.. autoapiclass:: UUID
    :no-index:
    :members:
    :undoc-members:
    :special-members:  

