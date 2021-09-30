from direct.showbase.DirectObject import DirectObject
from direct.task.TaskManagerGlobal import taskMgr
from direct.showbase.PythonUtil import bound

from panda3d.core import Vec3, Point2
from panda3d.bullet import BulletDebugNode

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape

# Class of the Physics world!!
# add and remove objects

import objectphysics


class PhysicsWorld():

    def __init__(self, taskMgr):

        # task manager for window
        self.taskMgr = taskMgr

        # Bullet is standard unit (m, s, kg)
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

        # Debug
        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(True)
        debugNP = render.attachNewNode(debugNode)
        debugNP.show()

        # Add node
        self.world.setDebugNode(debugNP.node())

        # Ground Plane
        ground = BulletPlaneShape(Vec3(0, 0, 1), 1)

        node = BulletRigidBodyNode('Ground')
        node.addShape(ground)

        np = render.attachNewNode(node)
        np.setPos(0, 0, -1)

        self.world.attachRigidBody(node)

    # Getter
    def addObject(self, object):
        self.world.attachRigidBody(object.node)

    def removeObject(self):
        pass
