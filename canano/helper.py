from enum import Enum

# RPI pin to trigger relay.
pin = 4


class State(Enum):
    ON = 1
    OFF = 0


class SetState:
    def on(self):
        self.state = State.ON

    def off(self):
        self.state = State.OFF

    def reset(func):
        def wrapper(self, *args, **kwargs):
            self.state = State.OFF
            if callable(func):
                func(self, *args, **kwargs)
            self.state = State.ON

        return wrapper if callable(func) else wrapper(func)


reset = SetState.reset
