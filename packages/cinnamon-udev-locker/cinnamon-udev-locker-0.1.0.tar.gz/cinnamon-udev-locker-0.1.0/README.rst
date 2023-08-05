cinnamon-udev-locker
====================

.. image:: https://img.shields.io/pypi/v/cinnamon-udev-locker.svg
    :target: https://pypi.python.org/pypi/cinnamon-udev-locker
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/fladi/cinnamon-udev-locker.png
   :target: https://travis-ci.org/fladi/cinnamon-udev-locker
   :alt: Latest Travis CI build status

Lock Cinnamon desktop session through device status (i.e YubiKey)

Usage
-----

Run in INIT mode with an empty YAML configuration:

    > touch ~/.config/cinnamon-udev-locker/config.yml
    > cinnamon-udev-locker --init

This will print out all available properties for a UDev event. With a YubiKey
just plug it in after executing the above steps and it will output something
like this:

    add:
    * ACTION: add
    * BUSNUM: 003
    * DEVNAME: /dev/bus/usb/003/030
    * DEVNUM: 030
    * DEVPATH: /devices/pci0000:00/0000:00:14.0/usb3/3-1/3-1.1
    * DEVTYPE: usb_device
    * DRIVER: usb
    * ID_BUS: usb
    * ID_FOR_SEAT: usb-pci-0000_00_14_0-usb-0_1_1
    * ID_MODEL: Yubikey_4_U2F+CCID
    * ID_MODEL_ENC: Yubikey\x204\x20U2F+CCID
    * ID_MODEL_FROM_DATABASE: Yubikey 4 U2F+CCID
    * ID_MODEL_ID: 0406
    * ID_PATH: pci-0000:00:14.0-usb-0:1.1
    * ID_PATH_TAG: pci-0000_00_14_0-usb-0_1_1
    * ID_REVISION: 0427
    * ID_SERIAL: Yubico_Yubikey_4_U2F+CCID
    * ID_SMARTCARD_READER: 1
    * ID_SMARTCARD_READER_DRIVER: gnupg
    * ID_USB_INTERFACES: :030000:0b0000:
    * ID_VENDOR: Yubico
    * ID_VENDOR_ENC: Yubico
    * ID_VENDOR_FROM_DATABASE: Yubico.com
    * ID_VENDOR_ID: 1050
    * MAJOR: 189
    * MINOR: 285
    * PRODUCT: 1050/406/427
    * SEQNUM: 3746
    * SUBSYSTEM: usb
    * SYSTEMD_WANTS: smartcard.target
    * TAGS: :uaccess:systemd:seat:
    * TYPE: 0/0/0
    * USEC_INITIALIZED: 359396531717

You can now create rules in the config file based on the above attributes and
their values. Values are matched against regular expressions to provide more
felxibility.

To have the screen locked when a YubiKey is disconnected and
to activate the password prompt to unlock the screen once it is reconnected, use
the following rule in `~/.config/cinnamon-udev-locker/config.yml`:

    ---
    - devices:
      - ID_VENDOR: ^Yubico$
        ID_MODEL: ^Yubikey.*
      add: wakeup
      remove: lock

It is possible to define more than one rule with different behaviours. To have a
second device that only activates the password prompt on connect but does not
lock the screen on disconnect just append to the YAML list of rules:

    ---
    - devices:
      - ID_VENDOR: ^Yubico$
        ID_MODEL: ^Yubikey.*
      add: wakeup
      remove: lock
    - devices:
      - ID_VENDOR: ^ACME$
        ID_MODEL_FROM_DATABASE: ^Detonator$
      add: wakeup

Afterwards make sure to have `cinnamon-udev-locker` automatically started for
your Cinnamon session.

Installation
------------

    pip install cinnamon-udev-locker

Requirements
^^^^^^^^^^^^

  * click
  * click-log
  * pygobject
  * pyxdg

Compatibility
-------------

This script was written for Python3 only.

Licence
-------

Published under MIT/Expat license.

Authors
-------

`cinnamon-udev-locker` was written by `Michael Fladischer <michael@fladi.at>`_.
