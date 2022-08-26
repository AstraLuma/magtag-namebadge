#!/usr/bin/python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: FAFOL

import time

import alarm
import board
import mdns
import socketpool
import wifi

from adafruit_magtag.magtag import MagTag

from name import NameDisplay, NameTag
from finger import FingerServ

# Get wifi details and more from a secrets.py file
try:
    from secrets import name, secrets
except ImportError:
    print("WiFi and name secrets are kept in secrets.py, please add them there!")
    raise

FINGER_PORT = 79


class TagFinger(FingerServ):
    @property
    def persona(self):
        return name[DISPLAY]

    @property
    def personas(self):
        yield from name.values()

    def find_persona(self, handle):
        for p in self.personas:
            if p.get('handle', None) == handle:
                return p
    
    def user_info(self, send, username, *, verbose):
        user = self.find_persona(username)
        if user:
            send(f"Login: {user['handle']}\n")
            send(f"Name: {user['name1']} {user['name2']}\n")
            send(f"Pronouns: {'/'.join(user['pronouns'])}\n")
        else:
            send('no. user does not exist.')

    def list_users(self, send, *, verbose):
        cur = self.persona
        for p in self.personas:
            if p:
                send(f"{p['handle']}\n")


wifi.radio.hostname = secrets['hostname']
wifi.radio.connect(secrets["ssid"], secrets["password"])

server = mdns.Server(wifi.radio)
server.hostname = wifi.radio.hostname
server.advertise_service(service_type='_finger', protocol='_tcp', port=FINGER_PORT)

magtag = MagTag()

DISPLAYS = NameTag(magtag=magtag, name=name)
DISPLAY = 'A'
DISPLAYS.render(display=DISPLAY)

fingerd = TagFinger()

# TODO: IPv6
pool = socketpool.SocketPool(wifi.radio)
sock = pool.socket()

sock.bind((str(wifi.radio.ipv4_address), FINGER_PORT))
sock.listen(2)

print("Listening")
while True:
    conn, addr = sock.accept()
    print("Connected to", addr)
    fingerd(conn)

while True:
    for i, b in enumerate(magtag.peripherals.buttons):
        if not b.value:
            DISPLAY = 'ABCD'[i]
            print(f'Button {DISPLAY} pressed')
            DISPLAYS.render(display=DISPLAY)
            break
    time.sleep(0.01)