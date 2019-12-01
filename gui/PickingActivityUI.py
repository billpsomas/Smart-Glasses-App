from gui.core.UINode import UINode
import utils.commons
from enums.UIState import UIState
from enums.PickingActivityState import PickingActivityState
from models.PickingActivityModel import PickingActivityModel
import gui.ActivityListUI
import time
import math
from utils.camera_utils import get_snapshot_rasbery
from utils.BarcodeRecogniton import recognize_barcode

class PickingActivityUI(UINode):

    SCANNING_MSG_FONT = utils.commons.make_font(utils.commons.DEFAULT_FONT_FILE, 14)
    SCANNING_ICON_FONT = utils.commons.make_font(utils.commons.FONT_AWESOME_FONT_FILE, 22)

    BOX_ICON_FONT = utils.commons.make_font(utils.commons.FONT_AWESOME_FONT_FILE, 22)
    NEXT_PREVIOUS_ICON_FONT = utils.commons.make_font(utils.commons.FONT_AWESOME_FONT_FILE, 10)

    TITLE_FONT = utils.commons.make_font(utils.commons.DEFAULT_FONT_FILE, 14)
    SUBTITLE_FONT = utils.commons.make_font(utils.commons.DEFAULT_FONT_FILE, 12)
    MULTIPLIER_FONT = utils.commons.make_font(utils.commons.DEFAULT_FONT_FILE, 18)

    def __init__(self, model: PickingActivityModel):
        super().__init__(UIState.PickingActivity)

        # Time passed after a selection
        self.timer: int = 0

        self.model: PickingActivityModel = model
        # Activity process step
        self.step: PickingActivityState = PickingActivityState.PICK_BOX
        # Time when activity started
        self.startTime: int = 0
        # Time when activity ended
        self.endTime: int = 0
        # Code scanning flag
        self.isScanninig: bool = False
        # Code of the selected box
        self.box: str = None

        # Current location index
        self.locationIndex: int = 0
        self.targetLocation = None
        self.selectedLocation: str = None

        self.productIndex: int = 0
        self.targetProduct = None
        self.selectedProduct: str = None

    def render(self, engine):
        
        if (self.startTime == 0):
            self.startTime = utils.commons.get_time_as_millis()

        # TOP PANEL
        engine.text((5, 2), text=utils.commons.getTimeFormatted(), font=utils.commons.TOP_PANEL_FONT, fill="white")
        engine.text((60, 2), text=utils.commons.ICONS.get("hashtag"), font=utils.commons.TOP_PANEL_ICON_FONT, fill="white")
        engine.text((73, 1), text=str(utils.state_manager.USER.ranking), font=utils.commons.TOP_PANEL_FONT, fill="white")
        engine.text((95, 3), text=utils.commons.ICONS.get("angle-double-up"), font=utils.commons.TOP_PANEL_ICON_FONT, fill="white")
        engine.text((103, 1), text=str(utils.state_manager.USER.points), font=utils.commons.TOP_PANEL_FONT, fill="white")

        # Timer
        if (self.step == PickingActivityState.GO_TO_LOCATION or self.step == PickingActivityState.PICK_PRODUCT):
            self.renderTimer(engine)

        # Main Content
        if (self.isScanninig):
            self.renderScanning(engine)
        else:
            if (self.step == PickingActivityState.PICK_BOX):
                self.renderPickBox(engine)
            elif (self.step == PickingActivityState.GO_TO_LOCATION):
                self.renderGoToLocation(engine)
            elif (self.step == PickingActivityState.PICK_PRODUCT):
                self.renderPickProduct(engine)
            elif (self.step == PickingActivityState.END):
                self.renderEnd(engine)

            # self.renderFooter(engine)


    def onVoiceCommand(self, command: str):
        # Runs in a background thread
        if (self.step == PickingActivityState.PICK_BOX):
            if (command == "SCAN" and self.box is None):
                self.isScanninig = True
                # Scan bar code here
                self.box = self.get_barcode()
                self.isScanninig = False

        elif (self.step == PickingActivityState.GO_TO_LOCATION):
            if (command == "SCAN" and self.selectedLocation is None):
                self.isScanninig = True
                # Scan bar code here
                self.selectedLocation = self.get_barcode()
                self.isScanninig = False

        elif (self.step == PickingActivityState.PICK_PRODUCT):
            if (command == "SCAN" and self.selectedProduct is None):
                self.isScanninig = True
                # Scan bar code here
                self.selectedProduct = self.get_barcode()
                self.isScanninig = False

    def renderTimer(self, engine):

        if (self.model.timer > 0):
            timer: int = self.model.timer - (utils.commons.get_time_as_millis() - self.startTime)

            if (timer > 0):
                minutes = math.floor((timer % (1000 * 60 * 60)) / (1000 * 60))
                seconds = math.floor((timer % (1000 * 60)) / 1000)

                utils.commons.text_center(engine, 25, text="{:02d}:{:02d}".format(minutes, seconds), font=utils.commons.DEFAULT_FONT, fill="white")
            else:
                utils.commons.text_center(engine, 25, text="{:02d}:{:02d}".format(0,0), font=utils.commons.DEFAULT_FONT, fill="white")

    def renderScanning(self, engine):
        
        utils.commons.text_center(engine, 50, text="Scanning...", font=PickingActivityUI.SCANNING_MSG_FONT, fill="white")
        engine.text((50,75), text=utils.commons.ICONS.get("camera"), font=PickingActivityUI.SCANNING_ICON_FONT, fill="white")

    def renderFooter(self, engine):

        engine.text((50,95), text=utils.commons.ICONS.get("map-marker-alt"), font=PickingActivityUI.NEXT_PREVIOUS_ICON_FONT, fill="white")
        engine.text((50,110), text=utils.commons.ICONS.get("box-open"), font=PickingActivityUI.NEXT_PREVIOUS_ICON_FONT, fill="white")

    def renderPickBox(self, engine):

        if (self.box is None):
            utils.commons.text_center(engine, 40, text="Pick up a box", font=PickingActivityUI.TITLE_FONT, fill="white")
            engine.text((50,60), text=utils.commons.ICONS.get("box-open"), font=PickingActivityUI.SCANNING_ICON_FONT, fill="white")

        else:

            self.goToNextLocation()

            # if (self.timer == 0):
            #     self.timer = utils.commons.get_time_as_millis()

            # if (utils.commons.get_time_as_millis() - self.timer > 3000):
            #     self.timer = 0

            #     self.goToNextLocation()

            # utils.commons.text_center(engine, 60, text="You got box with code 1234", font=utils.commons.DEFAULT_FONT, fill="white")

    def renderGoToLocation(self, engine):

        if (self.selectedLocation is None):
            utils.commons.text_center(engine, 40, text="Go to", font=PickingActivityUI.SUBTITLE_FONT, fill="white")
            utils.commons.text_center(engine, 60, text=self.targetLocation[0], font=PickingActivityUI.TITLE_FONT, fill="white")
            engine.text((52,80), text=utils.commons.ICONS.get("map-marker-alt"), font=PickingActivityUI.SCANNING_ICON_FONT, fill="white")

        elif (self.selectedLocation != self.targetLocation[1]):

            if (self.timer == 0):
                self.timer = utils.commons.get_time_as_millis()

            if (utils.commons.get_time_as_millis() - self.timer > 3000):
                self.timer = 0
                self.selectedLocation = None

            utils.commons.text_center(engine, 60, text="Wrong location!", font=PickingActivityUI.TITLE_FONT, fill="red")

        else:
            self.goToNextProduct()
            # Go directly to
            # self.goToNextProduct()
            # if (self.timer == 0):
            #     self.timer = utils.commons.get_time_as_millis()

            # if (utils.commons.get_time_as_millis() - self.timer > 3000):
            #     self.timer = 0

            #     self.goToNextProduct()

            # utils.commons.text_center(engine, 60, text="You got to the correct location", font=utils.commons.DEFAULT_FONT, fill="white")

    def renderPickProduct(self, engine):

        if (self.selectedProduct is None):
            utils.commons.text_center(engine, 45, text="Pick", font=PickingActivityUI.SUBTITLE_FONT, fill="white")
            utils.commons.text_center(engine, 60, text="{} x".format(self.targetProduct[1]), font=PickingActivityUI.MULTIPLIER_FONT, fill="white")
            utils.commons.text_center(engine, 80, text="{}".format(self.targetProduct[0][0]), font=PickingActivityUI.TITLE_FONT, fill="white")
            engine.text((50,100), text=utils.commons.ICONS.get("boxes"), font=PickingActivityUI.SCANNING_ICON_FONT, fill="white")

        elif (self.selectedProduct != self.targetProduct[0][1]):

            if (self.timer == 0):
                self.timer = utils.commons.get_time_as_millis()

            if (utils.commons.get_time_as_millis() - self.timer > 3000):
                self.timer = 0
                self.selectedProduct = None

            utils.commons.text_center(engine, 60, text="Wrong product!", font=PickingActivityUI.TITLE_FONT, fill="red")
        else:
            self.goToNextProduct()
            # if (self.timer == 0):
            #     self.timer = utils.commons.get_time_as_millis()

            # if (utils.commons.get_time_as_millis() - self.timer > 3000):
            #     self.timer = 0

            #     self.goToNextProduct()

            # utils.commons.text_center(engine, 60, text="You got the correct product", font=utils.commons.DEFAULT_FONT, fill="white")

    def renderEnd(self, engine):

        # if (self.timer == 0):
        #     self.timer = utils.commons.get_time_as_millis()

        # if (utils.commons.get_time_as_millis() - self.timer > 3000):
        #     utils.state_manager.APP.rootNode = gui.ActivityListUI.ActivityListUI()

        utils.commons.text_center(engine, 50, text="Timer Bonus!", font=PickingActivityUI.SUBTITLE_FONT, fill="white")
        utils.commons.text_center(engine, 70, text="+ 100", font=PickingActivityUI.TITLE_FONT, fill="white")


    def goToNextLocation(self):
        if (self.locationIndex < len(self.model.locations)):
            self.targetLocation = self.model.locations[self.locationIndex]
            self.productIndex = 0
            self.selectedLocation = None
            self.selectedProduct = None
            self.step = PickingActivityState.GO_TO_LOCATION
        else:
            self.locationIndex = 0
            self.productIndex = 0
            self.selectedLocation = None
            self.selectedProduct = None
            self.step = PickingActivityState.END

    def goToNextProduct(self):
        if (self.productIndex < len(self.model.locations[self.locationIndex][2])):
            self.targetProduct = self.model.locations[self.locationIndex][2][self.productIndex]
            self.productIndex += 1
            self.selectedProduct = None
            self.step = PickingActivityState.PICK_PRODUCT
        else:
            self.productIndex = 0
            self.locationIndex += 1
            self.selectedLocation = None
            self.selectedProduct = None

            self.goToNextLocation()

    def get_barcode(self):
        # photoshot the barcode
        get_snapshot_rasbery()
        barcode_string = recognize_barcode()
        return barcode_string