#!/usr/bin/env python
from in_place import InPlace

with InPlace("/boot/config.txt") as config:
    for line in config:
        config.write("".join(char for char in line))
    config.writelines(
        [
            "\n",
            "# Disable the splash screen\n",
            "disable_splash=1\n",
            "\n",
            "# Turn off boot delay\n",
            "boot_delay=0\n",
            "\n",
            "# Overclock the sd card\n",
            "dtoverlay=sdhost,overclock_50=100\n",
            "\n",
            "# Overclock the raspberry pi\n",
            "arm_freq=1050\n",
            "force_turbo=1\n",
        ]
    )
