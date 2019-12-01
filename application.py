from utils.commons import get_device
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator
from gui.core.UINode import UINode
from gui.SplashScreenUI import SplashScreenUI
# from utils.SpeechRecognitionTask import SpeechRecognitionTask
from utils.SpeechRecognitionTask_demo import SpeechRecognitionTask
import utils.state_manager

if __name__ == '__main__':

    device = get_device()
    regulator = framerate_regulator()
    speechRcTask = SpeechRecognitionTask()

    try:
        while True:
            with regulator:
                with canvas(device) as draw:
                    if (utils.state_manager.APP.rootNode is None):
                        utils.state_manager.APP.rootNode = SplashScreenUI()
                    
                    utils.state_manager.APP.rootNode.render(draw)

    except (KeyboardInterrupt, SystemExit):
       device.clear()
    finally:
       device.clear()

