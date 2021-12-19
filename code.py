import time

import alarm
from adafruit_magtag.magtag import MagTag

magtag = MagTag()

# Get nametag functions from name.py file
try:
    from name import *
except ImportError:
    print("WiFi and name secrets are kept in secrets.py, please add them there!")
    raise

# Get wifi details and more from a secrets.py file
try:
    from secrets import name, secrets
    DISPLAYS = NameTag(magtag=magtag, name=name)
except ImportError:
    print("WiFi and name secrets are kept in secrets.py, please add them there!")
    raise

# Check to see if we are in the first startup
if not alarm.wake_alarm:
    DISPLAY = 'A'
    DISPLAYS.render(display=DISPLAY)

while True:
    for i, b in enumerate(magtag.peripherals.buttons):
        if not b.value:
            DISPLAY = 'ABCD'[i]
            print(f'Button {DISPLAY} pressed')
            DISPLAYS.render(display=DISPLAY)
            break
    time.sleep(0.01)
