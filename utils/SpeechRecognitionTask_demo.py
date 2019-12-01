import time
import datetime
import threading
from enums.UIState import UIState
from gui.core.UINode import UINode
import utils.state_manager

class SpeechRecognitionTask():

    INTERVAL: int = 1

    def __init__(self):

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            # print(datetime.datetime.now().__str__() + ' : Start task in the background')

            currentNode: UINode = utils.state_manager.APP.rootNode

            if (currentNode is not None):
                if (currentNode.state == UIState.GamePromptScreen):
                    time.sleep(2)

                    # SIMULATE COMMAND
                    currentNode.onVoiceCommand("YES")

                elif (currentNode.state == UIState.ActivityList):
                    time.sleep(2)

                    # SIMULATE COMMAND
                    currentNode.onVoiceCommand("THREE")

                elif (currentNode.state == UIState.PickingActivity):
                    time.sleep(3)

                    # SIMULATE COMMAND
                    currentNode.onVoiceCommand("SCAN")


            time.sleep(SpeechRecognitionTask.INTERVAL)