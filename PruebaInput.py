from evdev import InputDevice, categorize, ecodes, KeyEvent

gamepad = InputDevice("/dev/input/event0")
print(gamepad)

#for event in gamepad.read_loop():
    #print(event)
while True:
    event = gamepad.read_one()
    if event != None:
        print(event)
