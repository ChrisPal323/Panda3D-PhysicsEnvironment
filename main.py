import sys
import random

from panda3d.core import WindowProperties
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
import gltf

from direct.filter.CommonFilters import CommonFilters
from direct.gui.DirectGui import *

from panda3d.core import loadPrcFile
loadPrcFile("config/conf.prc")

# Local Imports
import WorldConfig
import ObjectPhysics
import PlayerModel
import TextNodes


class SimplePhysicsEngine(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # create loader
        gltf.patch_loader(self.loader)

        # disable default mouse movement
        self.disable_mouse()

        # Window / Render properties
        props = WindowProperties()
        props.set_mouse_mode(WindowProperties.M_relative)
        base.win.request_properties(props)
        base.set_background_color(0.5, 0.5, 0.8)

        # Filters
        scene_filters = CommonFilters(base.win, base.cam)
        scene_filters.set_bloom()
        scene_filters.set_high_dynamic_range()
        scene_filters.set_exposure_adjust(1.1)
        scene_filters.set_gamma_adjust(1.1)

        # Set cam settings
        self.camLens.set_fov(80)
        self.camLens.set_near_far(0.01, 90000)
        self.camLens.set_focal_length(7)

        # Create Physics World
        self.world = WorldConfig.World(self.taskMgr, self.render, self.loader)

        # Game start bool
        self.game_start = 0

        # Create player with movement and camera
        self.player = PlayerModel.PlayerModel(self.render, self.world.world, self.camera, self.world.getShader())

        # Add text
        cordText = TextNodes.CustomTextNode('Cords', '(0, 0, 0)', (-1.7, 0, 0.92), 0.05, self.loader)

        # on-screen target dot for aiming
        targetDotText = TextNodes.CustomTextNode('DotAim', ".", (0, 0, 0), 0.075, self.loader)

        # Testing boxes!
        objectCount = 150

        # add a few random physics boxes
        for x in range(0, objectCount):
            # Create default cube
            cube = ObjectPhysics.BoxObject(self.render,  # Render
                                        self.world.world,  # World
                                        self.loader,  # Loader
                                        "random_cubes",  # Object Name
                                        (random.uniform(50, -50), random.uniform(50, -50), random.uniform(5, 10)),
                                        # Pos ^
                                        (random.uniform(0.5, 1.5), random.uniform(0.5, 1.5), random.uniform(0.5, 1.5)),  # Shape
                                        1,  # Mass
                                        20,  # Friction
                                        'media/models/1m_cube.gltf',  # Path
                                        (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1))  # Color

            ball = ObjectPhysics.BallObject(self.render,  # Render
                                        self.world.world,  # World
                                        self.loader,  # Loader
                                        "random_ball",  # Object Name
                                        (random.uniform(50, -50), random.uniform(50, -50), random.uniform(5, 10)),
                                        # Pos ^
                                        random.uniform(0.5, 1.5),  # Radius
                                        1,  # Mass
                                        10,  # Friction
                                        'media/models/1m_ball.bam',  # Path
                                        (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1))  # Color

        # ----------- End game ---------------

        # Bullet debugger
        from panda3d.bullet import BulletDebugNode
        debugNode = BulletDebugNode('Debug')
        debugNode.show_wireframe(True)
        debugNode.show_constraints(True)
        debugNode.show_bounding_boxes(False)
        debugNode.show_normals(False)
        debugNP = self.render.attach_new_node(debugNode)
        self.world.world.set_debug_node(debugNP.node())

        # pause menu
        self.pause_isHidden = True

        def toggle_pause():
            if self.pause_isHidden:

                self.pause_isHidden = False
                nunito_font = self.loader.load_font('media/fonts/Nunito/Nunito-Light.ttf')

                # 'pause'
                self.task_mgr.remove('Player Move')
                self.task_mgr.remove('General Update')
                self.task_mgr.remove('Physics Update')

                # Release Mouse
                self.player.turnOnRecenter()

                # Show
                self.pauseBg = OnscreenImage(
                    image="media/img/pause.png",
                    scale=(1.8, 1.5, 1))

                self.exitButton = DirectButton(
                    text="Exit Game", text_font=nunito_font,
                    scale=0.15, command=exitGame,
                    pad=(0.3, 0.3),
                    pos=(0, 0, -0.2))

                self.resumeButton = DirectButton(
                    text="Resume Game", text_font=nunito_font,
                    scale=0.15, command=toggle_pause,
                    pad=(0.3, 0.3),
                    pos=(0, 0, 0.2))

                # turn on mouse visible
                props = WindowProperties()
                props.setCursorHidden(False)
                base.win.requestProperties(props)

                # cancel control
                self.player.turnOffRecenter()

            else:

                # Add tasks back
                self.task_mgr.add(self.player.move, 'Player Move')
                self.task_mgr.add(update, 'General Update')
                self.task_mgr.add(physics_update, 'Physics Update')

                # Hide pause menu
                self.resumeButton.destroy()
                self.exitButton.destroy()
                self.pauseBg.destroy()
                # set bool
                self.pause_isHidden = True
                # Recenter mouse
                self.player.turnOnRecenter()
                # turn off mouse visible
                props = WindowProperties()
                props.setCursorHidden(True)
                base.win.requestProperties(props)

        # Exit function
        def exitGame():
            sys.exit()

        # debug toggle function
        def toggle_debug():
            if debugNP.is_hidden():
                debugNP.show()
            else:
                debugNP.hide()

        self.accept('f1', toggle_debug)
        self.accept("f3", self.toggle_wireframe)
        self.accept("escape", toggle_pause)

        # General Updates
        def update(Task):
            if self.game_start < 1:
                self.game_start = 1

            # Update Text
            cordText.updateText(
                f"({round(self.player.getX(), 1)}, {round(self.player.getY(), 1)}, {round(self.player.getZ(), 1)})")

            return Task.cont

        # Physics Updates
        def physics_update(Task):
            dt = globalClock.get_dt()
            self.world.world.do_physics(dt)
            return Task.cont

        # Attach to manager
        self.task_mgr.add(self.player.move, 'Player Move')
        self.task_mgr.add(update, 'General Update')
        self.task_mgr.add(physics_update, 'Physics Update')


app = SimplePhysicsEngine()
app.run()
