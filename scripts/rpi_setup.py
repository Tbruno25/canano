#!/usr/bin/env python
from in_place import InPlace

with InPlace("/boot/config.txt") as config:
    for line in config:
        if "dtparam=spi" in line:
            config.write("dtparam=spi=on\n")
        else:
            config.write("".join(char for char in line))
    config.writelines(
        [
            "\n",
            "# Enable canano module\n",
            "dtoverlay=spi-bcm2835-overlay\n"
            "dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25\n",
        ]
    )

with InPlace("/etc/network/interfaces") as interfaces:
    for line in interfaces:
        interfaces.write("".join(char for char in line))
    interfaces.writelines(
        [
            "\n",
            "# Enable can interface on boot\n",
            "auto can0\n",
            "iface can0 inet manual\n",
            "     pre-up ip link set $IFACE type can bitrate 500000\n",
            "     up /sbin/ifconfig $IFACE up\n",
            "     down /sbin/ifconfig $IFACE down\n",
        ]
    )
