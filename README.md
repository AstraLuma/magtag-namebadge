# MagTag Name Badge

This uses an [Adafruit MagTag](https://www.adafruit.com/product/4800) as a convention-style name badge.

## Displays

Four displays can be loaded, with defaults. Configure these in `secrets.py`, example below:
```python
# This file is where you keep secret settings, passwords, and tokens!
# If you put them in the code you risk committing that info or sharing it

secrets = {
    'ssid': 'your_wifi_ssid_here',
    'password': 'your_wifi_password_here',
    'aio_username': 'your_adafruitio_username_here',
    'aio_key': 'your_adafruitio_key_here',
    'timezone': "America/Detroit",  # http://worldtimeapi.org/timezones
}
name = {
    'A': # this display uses 100% of the defaults
    {},
    'B': # override the handle for this display using a ham callsign (mine!), maybe for a hamfest
    {
        'handle': 'KE8HOJ', 
    },
    'C': # override the handle for this display using a company name, maybe for a trade show
    {
        'handle': 'Company Name', 
    },
    'D': # override all fields for a DnD get-together
    {
        'name1': 'Thyia',
        'name2': 'Bonet',
        'handle': 'Half-Elf Bard',
        'pronouns': 'she/they'
    },
    '*': # these are defaults, used if the displays above are missing keys
    {
        'name1': 'Amelia',
        'name2': 'Meyer',
        'handle': 'AGMLego',
        'pronouns': 'she/her',
    },
}
```

To select the display, press the appropriate button. The corresponding NeoPixel will light, and a tone will play before and after the display is refreshed.

### Example Output

#### Display A
![Display A from above code](/samples/display_a.jpg)

#### Display B
![Display B from above code](/samples/display_b.jpg)

#### Display C
![Display C from above code](/samples/display_c.jpg)

#### Display D
![Display D from above code](/samples/display_d.jpg)
