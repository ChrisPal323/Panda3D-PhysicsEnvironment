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
import objectphysics

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
        self.font = self.loader.loadFont('media/fonts/Carlito-Regular.ttf')
        self.font.setPixelsPerUnit(100)
        self.font.setPageSize(512, 1024)
        loading = OnscreenText(text='Loading...',
                               scale=0.2,
                               pos=(0.0, 0.0),
                               fg=(1, 1, 1, 1),
                               shadow=(0.3, 0.3, 0.3, 1.0),
                               align=core.TextNode.ACenter,
                               mayChange=True,
                               font=self.font,
                               parent=self.aspect2d)

        self.graphicsEngine.renderFrame()  # Must render frame after text change for some
        self.graphicsEngine.renderFrame()  # Twice for some reason?

        loading.setText('Generating world')
        self.graphicsEngine.renderFrame()
        self.graphicsEngine.renderFrame()

        self.posText = OnscreenText(text="",
                                    scale=0.1,
                                    pos=(-1.15, 0.87),
                                    fg=(1, 1, 1, 1),
                                    shadow=(0.3, 0.3, 0.3, 1.0),
                                    align=core.TextNode.ACenter,
                                    mayChange=True,
                                    font=self.font,
                                    parent=self.aspect2d)

        # -------------------------  Physics  -------------------------------

        physicsWorld = worldphysics.PhysicsWorld(self.taskMgr)

        # Create box object (name, mass, shapeName, size)
        box = objectphysics.Object('Test Box', 1, 'box', Vec3(0.5, 0.5, 0.5))
        box.attachToRender(self.render)
        box.setPos(0, 0, 100)

        # Attach object
        physicsWorld.addObject(box)

        # create linear velocity
        box.createLinearVelocityArrow()

        def update(task):

            # Physics refresh
            dt = globalClock.getDt()
            physicsWorld.world.doPhysics(dt)

            # Update and clear pos text
            self.cameraPos = f"({round(self.camera.getX(), 1)}, {round(self.camera.getY(), 1)}, {round(self.camera.getZ(), 1)})"
            self.posText.text = self.cameraPos


            return task.cont

        taskMgr.add(update, 'update')

        # ----------------------------------------------------------------------

        loading.destroy()  # clear text
        self.font.setPageSize(256, 512)  # change size for cords

        self.camLens.setFocalLength(0.4)
        self.camera.setPos(-5, 0, 2)
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
