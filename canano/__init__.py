from . import pi, canano

for pin in pi.PinMap:
    globals()[pin.name] = canano.Component(pin)

canano = canano.Can(pi.Interface())
