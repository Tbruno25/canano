import RPi.GPIO as GPIO
from can import Bus

from .helper import reset, State, SetState


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
            GPIO.setup(self.obj.pin, state.value)


class Can(SetState):
    def __init__(self, interface_obj, type="socketcan"):
        self.interface = interface_obj
        self.type = type
        self.state = State(self.interface.state == "up")
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
    @reset
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
        self.interface.recovery()
        for rate in self.baudrates:
            self.baud = rate
            received = self.bus.recv(2)
            if received:
                return f"Baudrate successfully detected!"
        raise AttributeError("Something went wrong. Verify connections and try again.")
