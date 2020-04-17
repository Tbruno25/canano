
import RPi.GPIO as GPIO
import pysocketcan as pysc
from enum import Enum
from can import Bus


class State(Enum):
    ON = 1
    OFF = 0

class SetState:
    
    def on(self):
        self.state = State.ON

    def off(self):
        self.state = State.OFF


class PinMap(Enum):
    def __init__(self, pin, is_input):
        self.pin = pin
        self.is_input = is_input

    button = 21, True
    red_led = 6, False
    green_led = 13, False
    relay = 17, False


class Component(SetState):
    def __init__(self, pin_obj):
        self.obj = pin_obj

    @property
    def state(self):
        return State(GPIO.input(self.obj.pin))

    @state.setter
    def state(self, state):
        if self.obj.is_input:
            raise AttributeError("This component cannot be set")
        else:
            GPIO.output(self.obj.pin, state.value)


class Can(SetState):
    def __init__(self, type="socketcan"):
        self.type = type
        self.interface = pysc.Interface()
        self.interface.listen_only = True
        self.state = State(self.interface.state.value)
        self.baudrates = (  # Common automotive CAN bus speeds
            33000,
            100000,
            125000,
            250000,
            500000,
        )

    @property
    def state(self):
        return State(self._state)

    @state.setter
    def state(self, state):
        if state.value:
            self.bus = Bus(self.interface.id, bustype=self.type)
        else:
            self.bus.shutdown()
        self._state = state

    @property
    def baud(self):
        return self.interface.baud

    @baud.setter
    def baud(self, rate):
        if rate not in self.baudrates:
            return print(f"Invalid. Please choose from {self.baudrates}")
        self.interface.baud = rate

    def detect_baud(self):
        """
        Automatically attempt to detect baudrate.

        Sets interface to each available rate and listens.
        Exits if messages are received within 2.5 seconds.
        """
        for rate in self.baudrates:
            self.baud = rate
            received = self.bus.recv(2)
            if received:
                return f"Baudrate successfully detected!"
        raise AttributeError("Something went wrong. Verify connections and try again.")
