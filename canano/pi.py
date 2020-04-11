import RPi.GPIO as GPIO
import subprocess as sp

from .helper import reset, Enum, State, SetState


def run_script(script):
    """
    Runs script directly in RPI environment.
    """

    def run(script):
        return sp.check_output(script, shell=True).decode("utf8").strip()

    def wrapper(*args, **kwargs):
        return run(script(*args, **kwargs))

    return wrapper if callable(script) else run(script)


class PinMap(Enum):
    def __init__(self, pin, is_input):
        self.pin = pin
        self.is_input = is_input

    button = 21, True
    red_led = 6, False
    green_led = 13, False
    relay = 17, False


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
        return f"ip link set {self.id} " + ("down", "up")[state.value]

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
    def listen_only(self, state):
        return f"ip link set {self.id} type can listen-only {state.name.lower()}"

    @reset
    @run_script
    def recovery(self):
        return f"ip link set {self.id} type can restart-ms 100"

    @run_script
    def stream(self, args=""):
        return f"candump {args} {self.id}"


# Initialize pins on import
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in PinMap:
    if pin.is_input:
        GPIO.setup(pin.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    else:
        GPIO.setup(pin.pin, GPIO.OUT)
