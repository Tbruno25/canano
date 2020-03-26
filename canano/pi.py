import RPi.GPIO as GPIO
import subprocess as sp

from .helper import reset, pin, State, SetState

# Initialize pin for relay control.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)


def run_script(script):
    """
    Runs script directly in RPI environment.
    """

    def run(script):
        return sp.check_output(script, shell=True).decode("utf8").strip()

    def wrapper(*args, **kwargs):
        return run(script(*args, **kwargs))

    return wrapper if callable(script) else run(script)


class Interface(SetState):
    def __init__(self, id="can0"):
        self.id = id

    @property
    @run_script
    def state(self):
        return f"cat /sys/class/net/{self.id}/operstate"

    @state.setter
    @run_script
    def state(self, state):
        return f"ip link set {self.id} " + ("down", "up")[int(state.value)]

    @property
    @run_script
    def baud(self):
        return f"ip -det link show {self.id} | awk '/bitrate/ {{print $2}}'"

    @baud.setter
    @reset
    @run_script
    def baud(self, rate):
        return f"ip link set {self.id} type can bitrate {rate}"

    @reset
    @run_script
    def recovery(self):
        return f"ip link set {self.id} type can restart-ms 100"

    @run_script
    def stream(self, args=""):
        return f"candump {args} {self.id}"


interface = Interface()
