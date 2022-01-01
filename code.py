#!/usr/bin/python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: FAFOL

import time

import alarm
from adafruit_magtag.magtag import MagTag
import board

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
except ImportError:
    print("WiFi and name secrets are kept in secrets.py, please add them there!")
    raise

DISPLAYS = NameTag(magtag=magtag, name=name)

orig = None
DISPLAY = 'A'

# Check to see if we are in the first startup
if alarm.wake_alarm:
    orig = DISPLAY = chr(alarm.sleep_memory[0])
    if DISPLAY not in 'ABCD':
        # oh no
        DISPLAY = 'A'
        orig = None
    if isinstance(alarm.wake_alarm, alarm.time.TimeAlarm):
        # Do nothing, just let the button scan happen
        pass
    # TODO: Look for button

for i, b in enumerate(magtag.peripherals.buttons):
    if not b.value:
        DISPLAY = 'ABCD'[i]
        print(f'Button {DISPLAY} pressed')
        break

if orig != DISPLAY:
    DISPLAYS.render(display=DISPLAY)

alarm.sleep_memory[0] = ord(DISPLAY)

alarm.exit_and_deep_sleep_until_alarms(
    alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 5),
    # alarm.pin.PinAlarm(pin=board.D15, value=False, pull=True),
    # alarm.pin.PinAlarm(pin=board.D14, value=False, pull=True),
    # alarm.pin.PinAlarm(pin=board.D12, value=False, pull=True),
    # alarm.pin.PinAlarm(pin=board.D11, value=False, pull=True),
)
