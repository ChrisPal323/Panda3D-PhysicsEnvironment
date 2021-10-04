from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBaseGlobal import aspect2d

from panda3d.core import Vec3, Point3, BitMask32, LVecBase3f

from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import ZUp

from direct.actor.Actor import Actor


# Class for player configs
class PlayerModel(DirectObject):
    def __init__(self, render, world, camera, shader, targetDotText):

        self.render = render
        self.world = world
        self.camera = camera
        self.targetDotText = targetDotText

        self.game_start = 1

        # initialize player character physics the Bullet way
        shape_1 = BulletCapsuleShape(0.75, 0.5, ZUp)
        player_node = BulletCharacterControllerNode(shape_1, 0.1, 'Player')  # (shape, mass, player name)
        player_np = self.render.attach_new_node(player_node)
        player_np.set_pos(-20, -10, 30)
        player_np.set_collide_mask(BitMask32.allOn())
        self.world.attach_character(player_np.node())

        # cast player_np to self.player
        self.player = player_np

        # Grab model
        player_character = Actor("media/models/fullbody.bam")

        # reparent player character to render node / player model!
        fp_character = player_character
        fp_character.reparent_to(self.render)
        fp_character.set_scale(1)

        # set the actor shader
        fp_character.set_attrib(shader)

        # reparent at
        self.camera.reparent_to(self.player)

        # reparent character to FPS cam
        fp_character.reparent_to(self.player)
        fp_character.set_pos(0, 0, -0.95)
        self.camera.set_y(self.player, 0.03)
        self.camera.set_z(self.player, 0.5)

        # 3D player movement system begins
        self.keyMap = {"left": 0, "right": 0, "forward": 0, "backward": 0, "jump": 0}

        def setKey(key, value):
            self.keyMap[key] = value

        # define button map
        self.accept("w", setKey, ["forward", 1])
        self.accept("w-up", setKey, ["forward", 0])
        self.accept("s", setKey, ["backward", 1])
        self.accept("s-up", setKey, ["backward", 0])
        self.accept("a", setKey, ["left", 1])
        self.accept("a-up", setKey, ["left", 0])
        self.accept("d", setKey, ["right", 1])
        self.accept("d-up", setKey, ["right", 0])
        self.accept("space", setKey, ["jump", 1])
        self.accept("space-up", setKey, ["jump", 0])

        # the player movement speed
        self.movementSpeedForward = 9
        self.movementSpeedBackward = 5
        self.striveSpeed = 6
        self.dropSpeed = -0.5
        self.static_pos_bool = False
        self.static_pos = Vec3()

        self.recenterMouse = True

# ---------------------------------------

    def turnOffRecenter(self):
        self.recenterMouse = False

    def turnOnRecenter(self):
        self.recenterMouse = True

# ---------------------------------------

    def getX(self):
        return self.player.getX()

    def getY(self):
        return self.player.getY()

    def getZ(self):
        return self.player.getZ()

    # Nice ol' movement function
    # TODO : Make this better / refactor lol
    def move(self, Task):
        if self.game_start > 0:

            # get mouse data
            mouse_watch = base.mouseWatcherNode

            if mouse_watch.has_mouse():
                # get Mouse Pos
                posMouse = base.mouseWatcherNode.get_mouse()

                # Ray end points
                posFrom = Point3()
                posTo = Point3()

                # Find ray of looking
                base.camLens.extrude(posMouse, posFrom, posTo)
                posFrom = self.render.get_relative_point(base.cam, posFrom)
                posTo = self.render.get_relative_point(base.cam, posTo)
                rayTest = self.world.ray_test_closest(posFrom, posTo)
                target = rayTest.get_node()

                if target is not None and target.getMass() > 0:
                    # Set hitmarker color
                    self.targetDotText.setColor(0.9, 0.1, 0.1, 1)

                else:
                    # Just looking at nothing
                    self.targetDotText.setColor(1, 1, 1, 1)

            # get mouse data
            mouse_watch = base.mouseWatcherNode
            if mouse_watch.has_mouse():
                pointer = base.win.get_pointer(0)
                mouseX = pointer.get_x()
                mouseY = pointer.get_y()

            # screen sizes
            window_Xcoord_halved = base.win.get_x_size() // 2
            window_Ycoord_halved = base.win.get_y_size() // 2

            # mouse speed
            mouseSpeedX = 0.2
            mouseSpeedY = 0.2

            # maximum and minimum pitch
            maxPitch = 90
            minPitch = -50

            # cam view target initialization
            camViewTarget = LVecBase3f()

            if self.recenterMouse:
                # If here, not in pause menu

                if base.win.movePointer(0, window_Xcoord_halved, window_Ycoord_halved):
                    p = 0

                    if mouse_watch.has_mouse():

                        # calculate the pitch of camera
                        p = self.camera.get_p() - (mouseY - window_Ycoord_halved) * mouseSpeedY

                    # sanity checking
                    if p < minPitch:
                        p = minPitch
                    elif p > maxPitch:
                        p = maxPitch

                    if mouse_watch.has_mouse():
                        # directly set the camera pitch
                        self.camera.set_p(p)
                        camViewTarget.set_y(p)

                    # rotate the self.player's heading according to the mouse x-axis movement
                    if mouse_watch.has_mouse():
                        h = self.player.get_h() - (mouseX - window_Xcoord_halved) * mouseSpeedX

                    if mouse_watch.has_mouse():
                        # directly set the camera heading (yaw)
                        self.player.set_h(h)
                        camViewTarget.set_x(h)

                if self.keyMap["left"]:
                    if self.static_pos_bool:
                        self.static_pos_bool = False

                    self.player.set_x(self.player, -self.striveSpeed * globalClock.get_dt())

                if not self.keyMap["left"]:
                    if not self.static_pos_bool:
                        self.static_pos_bool = True
                        self.static_pos = self.player.get_pos()

                    self.player.set_x(self.static_pos[0])
                    self.player.set_y(self.static_pos[1])

                if self.keyMap["right"]:
                    if self.static_pos_bool:
                        self.static_pos_bool = False

                    self.player.set_x(self.player, self.striveSpeed * globalClock.get_dt())

                if not self.keyMap["right"]:
                    if not self.static_pos_bool:
                        self.static_pos_bool = True
                        self.static_pos = self.player.get_pos()

                    self.player.set_x(self.static_pos[0])
                    self.player.set_y(self.static_pos[1])

                if self.keyMap["forward"]:
                    if self.static_pos_bool:
                        self.static_pos_bool = False

                    self.player.set_y(self.player, self.movementSpeedForward * globalClock.get_dt())

                if self.keyMap["forward"] != 1:
                    if not self.static_pos_bool:
                        self.static_pos_bool = True
                        self.static_pos = self.player.get_pos()

                    self.player.set_x(self.static_pos[0])
                    self.player.set_y(self.static_pos[1])
                    self.player.set_z(self.player, self.dropSpeed * globalClock.get_dt())

                if self.keyMap["backward"]:
                    if self.static_pos_bool:
                        self.static_pos_bool = False

                    self.player.set_y(self.player, -self.movementSpeedBackward * globalClock.get_dt())

                if self.keyMap["jump"]:
                    if self.static_pos_bool:
                        self.static_pos_bool = False

                    if self.static_pos_bool:
                        self.static_pos_bool = False

                    self.player.node().do_jump()

        return Task.cont