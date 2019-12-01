from enum import Enum

class PickingActivityState(Enum):
    PICK_BOX = 1
    GO_TO_LOCATION = 2
    PICK_PRODUCT = 3
    END = 4