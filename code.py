#!/usr/bin/python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: FAFOL

import os

import rtc
import socketpool
import time
import wifi

from adafruit_magtag.magtag import MagTag
import adafruit_ntp
import circuitpython_schedule as schedule

magtag = MagTag()

print("Doing WiFi")
wifi.radio.hostname = os.getenv('WIFI_HOSTNAME', 'magtag')
wifi.radio.connect(
    os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD")
)

pool = socketpool.SocketPool(wifi.radio)

ntp = adafruit_ntp.NTP(
    pool,
    tz_offset=os.getenv("TZ_OFFSET", 0),
    socket_timeout=60,
)

magtag.add_text(
    text_position=(
        50,
        (magtag.graphics.display.height // 2) - 1,
    ),
    text_scale=3,
)

print("Grabbing time")
rtc.RTC().datetime = ntp.datetime


def refresh_display():
    print("Updating display")
    now = time.localtime()
    magtag.set_text(f"{now.tm_hour:02}:{now.tm_min:02}")


schedule.every(1).minute.do(refresh_display)


def sync_ntp():
    print("Resyncing Time")
    rtc.RTC().datetime = ntp.datetime


schedule.every(15).minutes.do(sync_ntp)


while True:
    schedule.run_pending()
    time.sleep(1)
