
from models.UserModel import UserModel
from threading import Lock
from gui.core.UINode import UINode
from models.ActivityModel import ActivityModel
from models.PickingActivityModel import PickingActivityModel

class Application:

    def __init__(self):
        self.lock = Lock()
        self._rootNode: UINode = None

    @property
    def rootNode(self):
        with self.lock:
            return self._rootNode

    @rootNode.setter
    def rootNode(self, node: UINode):
        with self.lock:
            self._rootNode = node

# Application
APP: Application = Application()

# User Data
USER: UserModel = UserModel()
USER.firstname = "Bill"
USER.lastname = "Psomas"
USER.ranking = 8
USER.points = 50

# Activities

ACTIVITIES = [
    ActivityModel("Loading/Unloading", "ONE"),
    ActivityModel("Put Away", "TWO"),
    ActivityModel("Picking", "THREE"),
    ActivityModel("Packing", "FOUR")
]

PICKING_ACTIVITY_MODEL: PickingActivityModel = PickingActivityModel()
# Seconds
PICKING_ACTIVITY_MODEL.timer = 100000
PICKING_ACTIVITY_MODEL.reward = 120
PICKING_ACTIVITY_MODEL.rewardMutli = 2

# List of locations
# each location is a tuple with name, code and a list of a tuples (product, qty)
# each product is a tuple with (name, code)
PICKING_ACTIVITY_MODEL.locations = [

    ("A1-05-02-01", "testbarcodeA", [
        (("5202310521010", "testbarcodeA"), 1)
    ]),

    ("A1-05-03-01", "testbarcodeA", [
        (("5202106183800", "testbarcodeA"), 2)
    ]),

    ("A1-06-03-01", "testbarcodeA", [
        (("5202114113113", "testbarcodeA"), 3)
    ])

]
