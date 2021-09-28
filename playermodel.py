from direct.showbase.DirectObject import DirectObject
from direct.task.TaskManagerGlobal import taskMgr
from direct.showbase.PythonUtil import bound

from panda3d.core import Vec3, Point2

# Class for player physics
# Mass of player
# How fast player is moving limbs
# momentum of player hitting into things
# How player falls

class PlayerModel():

    def __init__(self, mass, size):

        self.mass = mass
        self.size = size

    # find pos if right hand
    def find_right_hand_pos(self):
        pass

    # find pos of left hand
    def find_lef_hand_pos(self):
        pass
