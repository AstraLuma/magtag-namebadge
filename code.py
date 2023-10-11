#!/usr/bin/python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: FAFOL

import os

from adafruit_magtag.magtag import MagTag
import socketpool
import wifi

magtag = MagTag()

wifi.radio.hostname = os.getenv('WIFI_HOSTNAME', 'magtag')
wifi.radio.connect(
    os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD")
)

pool = socketpool.SocketPool(wifi.radio)
