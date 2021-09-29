import random
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage

import panda3d.core as core
from panda3d.core import CollisionSphere
from panda3d.core import NodePath
from panda3d.core import Vec3
from panda3d.core import CollisionHandlerQueue

import camera
import worldphysics

class SimplePhysicsEngine(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Name Frame
        wp = core.WindowProperties()
        wp.setTitle("Simple Physics Engine")
        wp.setSize(1080, 720)
        wp.setCursorHidden(True)
        self.win.requestProperties(wp)

        # Set render stuff
        self.setBackgroundColor(0.5, 0.5, 1)
        self.disableMouse()  # This name sucks, just disables default mouse

        # Physics Engine?
        self.enableParticles()

        # Font / text
        font = self.loader.loadFont('media/fonts/Carlito-Regular.ttf')
        font.setPixelsPerUnit(100)
        font.setPageSize(512, 1024)
        loading = OnscreenText(text='Loading...',
                               scale=0.2,
                               pos=(0.0, 0.0),
                               fg=(1, 1, 1, 1),
                               shadow=(0.3, 0.3, 0.3, 1.0),
                               align=core.TextNode.ACenter,
                               mayChange=True,
                               font=font,
                               parent=self.aspect2d)

        self.graphicsEngine.renderFrame()  # Must render frame after text change for some
        self.graphicsEngine.renderFrame()  # Twice for some reason?

        loading.setText('Generating world')
        self.graphicsEngine.renderFrame()
        self.graphicsEngine.renderFrame()

        self.scene = self.loader.loadModel("media/models/environment")
        self.scene.setScale(0.01, 0.01, 0.01)
        self.scene.setPos(0, 0, 0)
        self.scene.reparentTo(self.render)

        # -------------- Testing Panda3D Physics with sphere Soccerball -----------------

        self.physicsWorld = worldphysics.PhysicsWorld(self.taskMgr)

        def update(task):
            dt = globalClock.getDt()
            self.physicsWorld.world.doPhysics(dt)
            return task.cont

        taskMgr.add(update, 'update')

        # ----------------------------------------------------------------------

        loading.destroy()  # clear text a

        self.camLens.setFocalLength(0.4)
        self.camera.setPos(0, 0, 2)
        self.cam.setPos(0, 0, 0)
        self.cam.setHpr(0, -45, 0)

        # World Size!
        self.worldSize = core.LPoint3f(10, 10, 10)

        self.cc = camera.CameraController(self.worldSize,
                                          self.mouseWatcherNode,
                                          self.camera,
                                          self.cam,
                                          self.win)

    def add_light(self):
        x, y = random.choice(list(self.world.columns()))
        for z in reversed(range(self.world.depth)):
            b = self.world.get_block(x, y, z)
            if not b.is_void:
                p = core.PointLight('pl-{}-{}-{}'.format(x, y, z))
                p.setAttenuation(core.Point3(0, 0, 0.4))
                pn = self.render.attachNewNode(p)
                pn.setPos(x, y, z + 3)
                self.render.setLight(pn)


app = SimplePhysicsEngine()
app.run()
