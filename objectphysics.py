from direct.showbase.DirectObject import DirectObject
from direct.task.TaskManagerGlobal import taskMgr
from direct.showbase.PythonUtil import bound

from panda3d.core import Vec3, Point2

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape


# Class for player physics
# Mass of player
# How fast player is moving limbs
# momentum of player hitting into things
# How player falls

class Object():

    def __init__(self, mass, shape, size, world):
        self.mass = mass  # kg
        self.shape = shape  # just string of ball, box, ect
        self.size = size  # a Vec3

        # Box
        shape = BulletBoxShape(size)
        node = BulletRigidBodyNode(self.shape)
        node.setMass(mass)
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setPos(0, 0, 50)
        world.attachRigidBody(node)
        model = loader.loadModel('media/models/box.egg')
        model.flattenLight()
        model.reparentTo(np)