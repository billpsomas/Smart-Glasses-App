from gui.core.UINode import UINode
import utils.commons
from enums.UIState import UIState
from gui.ActivityListUI import ActivityListUI

class GamePromptUI(UINode):
    
    TITLE_TEXT: str = "Do you want to play?"
    SUBTITLE_TEXT: str = "Yes or No?"
    ICON_FONT = utils.commons.make_font(utils.commons.FONT_AWESOME_FONT_FILE, 18)
    TITLE_FONT = utils.commons.make_font(utils.commons.DEFAULT_FONT_FILE, 12)

    def __init__(self):
        super().__init__(UIState.GamePromptScreen)

    def render(self, engine):
        
        # TOP PANEL
        engine.text((5, 2), text=utils.commons.getTimeFormatted(), font=utils.commons.TOP_PANEL_FONT, fill="white")
        engine.text((60, 2), text=utils.commons.ICONS.get("hashtag"), font=utils.commons.TOP_PANEL_ICON_FONT, fill="white")
        engine.text((73, 1), text=str(utils.state_manager.USER.ranking), font=utils.commons.TOP_PANEL_FONT, fill="white")
        engine.text((95, 3), text=utils.commons.ICONS.get("angle-double-up"), font=utils.commons.TOP_PANEL_ICON_FONT, fill="white")
        engine.text((103, 1), text=str(utils.state_manager.USER.points), font=utils.commons.TOP_PANEL_FONT, fill="white")

        # BODY PANEL
        utils.commons.text_center(engine, 50, text=GamePromptUI.TITLE_TEXT, font=GamePromptUI.TITLE_FONT, fill="white")
        utils.commons.text_center(engine, 65, text=GamePromptUI.SUBTITLE_TEXT, font=utils.commons.DEFAULT_FONT, fill="white")
        engine.text((52, 85), text=utils.commons.ICONS.get("gamepad"), font=GamePromptUI.ICON_FONT, fill="white")

    def onVoiceCommand(self, command: str):
        if (command == "YES"):
            utils.state_manager.APP.rootNode = ActivityListUI()
