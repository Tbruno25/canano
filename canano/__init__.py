import pysocketcan
from .canano import Can, Component, PinMap, GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in PinMap:
    if pin.is_input:
        GPIO.setup(pin.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    else:
        GPIO.setup(pin.pin, GPIO.OUT)
    globals()[pin.name] = Component(pin)

canano = Can()
