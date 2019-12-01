import datetime
from gui.core.UINode import UINode
from enums.UIState import UIState
from utils.commons import DEFAULT_FONT, FONT_AWESOME_FONT_FILE, ICONS, right_text, make_font

class TopBarUI(UINode):

    def __init__(self):
        super().__init__(UIState.ActivityList)
        self._battery_level = 100
        self.fontawesome_font = make_font(FONT_AWESOME_FONT_FILE, 48)
        self.keys = list(ICONS.keys())
        self.index = 0
        self.iterations = 0

    def _getTime(self):
        return datetime.datetime.now().strftime("%d/%m/%y %H:%M %S")

    def render(self, engine):

        engine.text((0, 0), self._getTime(), font=DEFAULT_FONT, fill="white")
        right_text(engine, 0, 128, 0, text="{}%".format(self._battery_level))

        self.iterations += 1

        if (self.iterations > 20):
            self.iterations = 0
            self.index += 1

        if (self.index >= len(self.keys)):
            self.index = 0

        engine.text((40, 40), ICONS[self.keys[self.index]], font=self.fontawesome_font, fill="yellow")
        
