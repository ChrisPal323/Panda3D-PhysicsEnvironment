from direct.showbase.DirectObject import DirectObject
from direct.task.TaskManagerGlobal import taskMgr
from direct.showbase.PythonUtil import bound

from panda3d.core import Vec3, Point2


# Class of the Physics world!!
# add and remove objects

import objectphysics

class PhysicsWorld():

    def __init__(self, worldSize):
        # this size must match the environment or weirdness
        # we assume this is just a box
        # ex. (length, width, height)
        self.worldSize = worldSize

        # list of "objects"
        self.objects = []

        # GRavity!
        self.gravityVector = (0, 0, -9.81)

    # add object to list
    def add_object(self, name, object):
        objectNameAndClass = [name, object]
        self.objects.append(objectNameAndClass)

    # remove object by name
    def remove_object(self, name):
        for i in len(self.objects):
            if self.objects[i][0] is name:
                self.objects.remove(i)
                return

    # Iterate through all objects
    def step_through(self, deltaTime):
        for object in self.objects:

            # apply forces!! from equations
            # a = F/m  (subbed this out in equations)
            # v = v0 + (F/m)(t)
            # x = x0 + vt
            object.force += object.mass * self.gravityVector
            object.velocity += object.force / (object.mass * deltaTime)
            object.position += object.velocity * deltaTime

            # reset net force
            object.force = (0, 0, 0)

