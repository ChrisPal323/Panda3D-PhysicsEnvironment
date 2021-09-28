from direct.showbase.DirectObject import DirectObject
from direct.task.TaskManagerGlobal import taskMgr
from direct.showbase.PythonUtil import bound

from panda3d.core import Vec3, Point2


# Class for player physics
# Mass of player
# How fast player is moving limbs
# momentum of player hitting into things
# How player falls

class Object():

    def __init__(self, mass, size, shape):
        self.mass = mass
        self.size = size
        self.shape = shape  # just string of ball, cube, ect

        # ---- physics!-----
        # all three are 3Vectors
        self.position = (0, 0, 0)
        self.velocity = None
        self.force = None