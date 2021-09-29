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

    def __init__(self, objName, mass, shapeName, size):
        self.mass = mass  # kg
        self.shapeName = shapeName  # just string of ball, box, ect
        self.objName = objName
        self.size = size  # a Vec3
        self.node = None

        # Box
        nodeShape = BulletBoxShape(size)
        self.node = BulletRigidBodyNode(shapeName)
        self.node.setMass(mass)
        self.node.addShape(nodeShape)
        self.np = render.attachNewNode(self.node)

        # Model name string
        name = f'media/models/{shapeName}.egg'
        model = loader.loadModel(name)
        model.flattenLight()
        model.reparentTo(self.np)

    def setPos(self, x, y, z):
        self.np.setPos(x, y, z)
        pass