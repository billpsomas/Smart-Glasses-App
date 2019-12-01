from enums.UIState import UIState

class UINode:

    def __init__(self, state: UIState):
        self.state: UIState = state

    def render(self, engine):        
        raise NotImplementedError()

    def onVoiceCommand(self, command: str):
        pass