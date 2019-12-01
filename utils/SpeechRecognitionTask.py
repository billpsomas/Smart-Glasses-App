import datetime
import threading
from re import search

import speech_recognition as sr

import utils.state_manager
from gui.core.UINode import UINode

YES_ARRAY = ["yes", "TS"]
NO_ARRAY = ["no", "know", "new", "None", "none", "Nu"]
SCAN_ARRAY = ["scan", "scam", "gun", "gum", "scandal", "Skyrim", "scum", "can", "scone", "skin", "skunk", "scammed", "skam"]
ONE_ARRAY = ["one", "1", "wan", "want", "wont", "13:00", 'number one', 'number 1', 'Juan']
TWO_ARRAY = ['2', 'two', 'to', 'too', '2:00', 'number two', 'number 2', 'number to']
THREE_ARRAY = ['number three', 'number 3', '3', 'three', '3:00', '3', 'tree', ]
FOUR_ARRAY = ["four", 'number for', 'number four', 'number 4', 'the number 4', 'four', 'Ford', 'for', "4:00", "16:00", 'full', 'Foo', 'fool']


class SpeechRecognitionTask():
    global r
    r = sr.Recognizer()
    global mic
    mic = sr.Microphone()

    INTERVAL: int = 1

    def __init__(self):

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            print(datetime.datetime.now().__str__() + ' : Start task in the background')

            string = self.recognise_speech()
            interpretaions_list = self.interpretaion(string)
            print(interpretaions_list)
            intent = self.getIntent(interpretaions_list)
            print(intent)
            currentNode: UINode = utils.state_manager.APP.rootNode
            if currentNode is not None:
                currentNode.onVoiceCommand(intent)

                # if (currentNode.state == UIState.GamePromptScreen):
                #     time.sleep(3)
                #
                #     # SIMULATE COMMAND
                #     currentNode.onVoiceCommand(intent)
                #
                # elif (currentNode.state == UIState.ActivityList):
                #     time.sleep(2)
                #
                #     # SIMULATE COMMAND
                #     currentNode.onVoiceCommand(intent)
                #
                # elif (currentNode.state == UIState.PickingActivity):
                #     time.sleep(2)
                #
                #     # SIMULATE COMMAND
                #     currentNode.onVoiceCommand(intent)


            # time.sleep(SpeechRecognitionTask.INTERVAL)

    # Method make the speach recognition
    def recognise_speech(self):
        with mic as source:
            audio = r.listen(source, timeout=None, phrase_time_limit=5)
            recognition_dict = r.recognize_google(audio, key=None, language="el-GR", show_all=True)
            return recognition_dict


    def interpretaion(self, recognition_dict):
        if isinstance(recognition_dict, dict):
            alternatives_dictionary = recognition_dict['alternative']
            list_of_transcriptions = []
            for element in alternatives_dictionary:
                list_of_transcriptions.append(element['transcript'])
            return list_of_transcriptions

    def getIntent(self, interpretaions_list):
        if isinstance(interpretaions_list, list):
            for element in interpretaions_list:
                for keyword in YES_ARRAY:
                    if search(keyword, element):
                        return "YES"
                for keyword in NO_ARRAY:
                    if search(keyword, element):
                        return "NO"
                for keyword in SCAN_ARRAY:
                    if search(keyword, element):
                        return "SCAN"
                for keyword in ONE_ARRAY:
                    if search(keyword, element):
                        return "ONE"
                for keyword in TWO_ARRAY:
                    if search(keyword, element):
                        return "TWO"
                for keyword in THREE_ARRAY:
                    if search(keyword, element):
                        return "THREE"
                for keyword in FOUR_ARRAY:
                    if search(keyword, element):
                        return "FOUR"
            return None

    def interpretation_match(self, element, array, return_string):
        if isinstance(array, list):
            for keyword in array:
                if search(keyword, element):
                    return return_string
        return None
