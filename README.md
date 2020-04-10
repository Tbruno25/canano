# canano

Python library for Canano Raspberry Pi add-on board. <img align="right" src="https://i.ibb.co/FnDczVM/board2.jpg">


## Installation

Use [pip](https://pip.pypa.io/en/stable/) to install package on Raspberry Pi

```bash
pip install canano
```
Copy ```/scripts``` using [svn](https://subversion.apache.org/) or by cloning the repo
```bash
sudo svn checkout https://github.com/Tbruno25/canano/trunk/scripts
```

Run ```rpi_setup.py``` to modify ```/boot/config``` and ```/etc/network/interfaces```  for use with the canano board

```bash
sudo python3 scripts/rpi_setup.py
sudo reboot
```

## Usage
The api currently gives you control over the components on the board
```python
from canano import red_led, green_led, relay, button

red_led.on() # activate
green_led.off() # deactivate
button.state # returns state 
```
canano controls the socketcan interface allowing you to easily adjust on the fly
```python
from canano import canano
canano.baud = 250000 # sets bus baudrate to 250k
canano.reset() # clears buffer 
canano.bus # python-can bus object 
canano.bus.recv() # returns next message
```
Play around with it to find interesting use cases! 


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

<p align="center">
<img src="https://i.ibb.co/1XXtwDD/board.jpg">
</p