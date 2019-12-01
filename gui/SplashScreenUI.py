from gui.core.UINode import UINode
import utils.commons
from enums.UIState import UIState
import utils.state_manager
from gui.WelcomeScreenUI import WelcomeScreenUI

class SplashScreenUI(UINode):
    
    DURATION: int = 2000
    TITLE_TEXT: str = "1UP"
    ICON_FONT = utils.commons.make_font(utils.commons.FONT_AWESOME_FONT_FILE, 48)
    TITLE_FONT = utils.commons.make_font(utils.commons.DEFAULT_FONT_FILE, 18)

    def __init__(self):
        super().__init__(UIState.SplashScreen)

        self.startTime: int = 0

    def render(self, engine):
        
        if (self.startTime == 0):
            self.startTime = utils.commons.get_time_as_millis()

        if (utils.commons.get_time_as_millis() - self.startTime >= SplashScreenUI.DURATION):
            utils.state_manager.APP.rootNode = WelcomeScreenUI()
        else:
            engine.text((40, 20), text=utils.commons.ICONS.get("glasses"), font=SplashScreenUI.ICON_FONT, fill="white")
            utils.commons.text_center(engine, 75, text=SplashScreenUI.TITLE_TEXT, font=SplashScreenUI.TITLE_FONT, fill="white")
