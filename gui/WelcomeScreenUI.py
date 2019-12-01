from gui.core.UINode import UINode
import utils.commons
from enums.UIState import UIState
from gui.GamePromptUI import GamePromptUI

class WelcomeScreenUI(UINode):
    
    DURATION: int = 1000
    WELCOME_TEXT: str = "Welcome back"
    ICON_FONT = utils.commons.make_font(utils.commons.FONT_AWESOME_FONT_FILE, 28)
    TITLE_FONT = utils.commons.make_font(utils.commons.DEFAULT_FONT_FILE, 16)

    def __init__(self):
        super().__init__(UIState.WelcomeScreen)

        self.startTime: int = 0

    def render(self, engine):
        
        if (self.startTime == 0):
            self.startTime = utils.commons.get_time_as_millis()

        if (utils.commons.get_time_as_millis() - self.startTime >= WelcomeScreenUI.DURATION):
            utils.state_manager.APP.rootNode = GamePromptUI()
        else:
            # TOP PANEL
            engine.text((5, 2), text=utils.commons.getTimeFormatted(), font=utils.commons.TOP_PANEL_FONT, fill="white")
            engine.text((60, 2), text=utils.commons.ICONS.get("hashtag"), font=utils.commons.TOP_PANEL_ICON_FONT, fill="white")
            engine.text((73, 1), text=str(utils.state_manager.USER.ranking), font=utils.commons.TOP_PANEL_FONT, fill="white")
            engine.text((95, 3), text=utils.commons.ICONS.get("angle-double-up"), font=utils.commons.TOP_PANEL_ICON_FONT, fill="white")
            engine.text((103, 1), text=str(utils.state_manager.USER.points), font=utils.commons.TOP_PANEL_FONT, fill="white")

            # BODY PANEL
            utils.commons.text_center(engine, 30, text=WelcomeScreenUI.WELCOME_TEXT, font=WelcomeScreenUI.TITLE_FONT, fill="white")
            utils.commons.text_center(engine, 50, text=utils.state_manager.USER.firstname, font=WelcomeScreenUI.TITLE_FONT, fill="white")
            engine.text((50, 80), text=utils.commons.ICONS.get("smile"), font=WelcomeScreenUI.ICON_FONT, fill="white")
