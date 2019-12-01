from gui.core.UINode import UINode
import utils.commons
from enums.UIState import UIState
from models.ActivityModel import ActivityModel
from gui.PickingActivityUI import PickingActivityUI

class ActivityListUI(UINode):
    
    DURATION: int = 4000
    TITLE_TEXT: str = "Select your next activity:"
    TITLE_FONT = utils.commons.make_font(utils.commons.DEFAULT_FONT_FILE, 11)

    def __init__(self):
        super().__init__(UIState.ActivityList)

        self.startTime: int = 0

    def render(self, engine):
        
        if (self.startTime == 0):
            self.startTime = utils.commons.get_time_as_millis()

        # if (utils.commons.get_time_as_millis() - self.startTime >= WelcomeScreenUI.DURATION):
        #     print("finished")
        # else:

        # TOP PANEL
        engine.text((5, 2), text=utils.commons.getTimeFormatted(), font=utils.commons.TOP_PANEL_FONT, fill="white")
        engine.text((60, 2), text=utils.commons.ICONS.get("hashtag"), font=utils.commons.TOP_PANEL_ICON_FONT, fill="white")
        engine.text((73, 1), text=str(utils.state_manager.USER.ranking), font=utils.commons.TOP_PANEL_FONT, fill="white")
        engine.text((95, 3), text=utils.commons.ICONS.get("angle-double-up"), font=utils.commons.TOP_PANEL_ICON_FONT, fill="white")
        engine.text((103, 1), text=str(utils.state_manager.USER.points), font=utils.commons.TOP_PANEL_FONT, fill="white")

        # BODY PANEL
        # TITLE
        engine.text((5, 30), text=ActivityListUI.TITLE_TEXT, font=ActivityListUI.TITLE_FONT, fill="white")

        # ACTIVITY LIST
        index: int = 0
        y: int = 30
        for activity in utils.state_manager.ACTIVITIES:
            index += 1
            y += 15
            self.printActivity(engine, index, y, activity)

    def printActivity(self, engine, index: int, y: int, activity: ActivityModel):
        engine.text((5, y), text="{}. {}".format(index, activity.name), font=utils.commons.DEFAULT_FONT, fill="white")

    def onVoiceCommand(self, command: str):
        if (command == "THREE"):
            # PICKING
            utils.state_manager.APP.rootNode = PickingActivityUI(utils.state_manager.PICKING_ACTIVITY_MODEL)