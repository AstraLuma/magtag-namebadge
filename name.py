from adafruit_magtag.magtag import MagTag


class NameDisplay():
    def __init__(self, magtag: MagTag, index: int, color: int, tone: int,
                 name1: str = None, name2: str = None,
                 handle: str = None, pronouns: str = None) -> 'NameDisplay':
        """
        Create a display

        Args:
            magtag (MagTag): Reference to display
            index (int): Which display is this?
            color (int): RGB color for associated NeoPixel
            tone (int): Frequency in Hz for button sound
            name1 (str): First line of name, rendered largest (default None)
            name2 (str): Second line of name, rendered smaller (default None)
            handle (str): Handle, rendered same as name2 (default None)
            pronouns (str): Pronoun reference, rendered smallest (default None)

        """
        self.magtag = magtag
        self.index = index

        self.name1 = name1
        self.name2 = name2
        self.handle = handle
        self.pronouns = pronouns

        colors = [0, 0, 0, 0]
        colors[index] = color
        self.button_color = colors
        self.button_color.reverse()  # the natural order is backwards...
        self.button_tone = tone

    def render(self) -> None:
        """
        Render this display to the magtag
        """
        print(
            f'Rendering:\n\t{self.name1}\n\t\t{self.name2}\n\t\t{self.handle}\n\t\t{self.pronouns}')

        # light chosen display NeoPixel
        self.magtag.peripherals.neopixel_disable = False
        self.magtag.peripherals.neopixels[0:4] = self.button_color
        self.magtag.peripherals.neopixels.show()

        # play a tone to indicate start of render
        self.magtag.peripherals.play_tone(self.button_tone, 0.25)

        # render text fields
        if self.name1 is not None:
            self.magtag.set_text(self.name1, 0, auto_refresh=False)
        if self.name2 is not None:
            self.magtag.set_text(self.name2, 1, auto_refresh=False)
        if self.handle is not None:
            self.magtag.set_text(f'({self.handle})', 2, auto_refresh=False)
        if self.pronouns is not None:
            self.magtag.set_text(
                f'Please use {self.pronouns.upper()} pronouns', 3, auto_refresh=False)
        self.magtag.refresh()

        # play a tone to indicate end of render
        self.magtag.peripherals.play_tone(self.button_tone + 250, 0.25)

        # turn off NeoPixels
        self.magtag.peripherals.neopixel_disable = True


class NameTag(dict):
    def __init__(self, magtag: MagTag, name: dict) -> 'NameTag':
        """
        Build up the name dictionary, using defaults as needed

        Args:
            magtag (MagTag): Reference to display
            name (dict): A dictionary with keys for each button, and a '*' for defaults
                            Subkeys should be 'name1', 'name2', 'handle', and 'pronouns'

        """
        self.magtag = magtag
        self.displays = {}
        colors = {
            'A': 0xFF0000,
            'B': 0x00FF00,
            'C': 0x0000FF,
            'D': 0x00FFFF,
        }
        tones = {
            'A': 1047,
            'B': 1318,
            'C': 1568,
            'D': 2093
        }
        buttons = 'ABCD'
        for button in buttons:
            self.displays[button] = NameDisplay(
                magtag=self.magtag,
                index=buttons.find(button),
                color=colors[button],
                tone=tones[button])

            for item in ('name1', 'name2', 'handle', 'pronouns'):
                try:
                    value = name[button][item]
                except KeyError:
                    try:
                        value = name['*'][item]
                    except KeyError:
                        value = None
                setattr(self.displays[button], item, value)

        # name1 field
        self.magtag.add_text(
            text_font="/fonts/Arial-18.pcf",
            text_position=(10, 20),
            text_scale=2,
            text_color=0x000000,
        )
        # name2 field
        self.magtag.add_text(
            text_font="/fonts/Arial-18.pcf",
            text_position=(10, 60),
            text_scale=1,
            text_color=0x202020,
        )
        # handle field
        self.magtag.add_text(
            text_font="/fonts/Arial-18.pcf",
            text_position=(10, 90),
            text_scale=1,
            text_color=0x404040,
        )
        # pronouns field
        self.magtag.add_text(
            text_font="/fonts/Arial-14.pcf",
            text_position=(10, 110),
            text_scale=1,
            text_color=0x404040,
        )
        self.magtag.preload_font()

    def __getitem__(self, __k: str) -> NameDisplay:
        return self.displays[__k]

    def __len__(self) -> int:
        return self.displays.__len__()

    def render(self, display: str = 'A') -> None:
        """
        Render the selected display to the magtag

        Args:
            display (str, optional): The display to render, one of 'A', 'B', 'C', or 'D'. Defaults to 'A'.
        """
        assert(display in self.displays)
        self.displays[display].render()
