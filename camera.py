from direct.showbase.DirectObject import DirectObject
from direct.task.TaskManagerGlobal import taskMgr
from direct.showbase.PythonUtil import bound

from panda3d.core import Vec3, Point2

import playermodel

class CameraController(DirectObject):
    def __init__(self, extents, mouse, body, eye, window):
        self.extents = extents
        self.body = body
        self.eye = eye

        self.mouse = mouse
        self.window = window

        self.keys = {
            'w': False,
            's': False,
            'd': False,
            'a': False,
            'space': False,
            'lshift': False
        }

        self.lookAround = None
        self.moving = False
        self.panning = False  # World extents!
        self.pause = False

        self.accept_keyboard()
        self.accept('console-open', self.ignore_keyboard)
        self.accept('console-close', self.accept_keyboard)

        self.accept('escape', self.show_pause_menu)
        self.accept('escape', self.close_pause_menu)

        self.accept('mouse3', self.start_lookAround)
        self.accept('mouse3-up', self.end_lookAround)

        taskMgr.add(self.move_camera, "Move Camera")

    def accept_keyboard(self):
        for k in self.keys:
            self.accept(k, self.key, [k, True])
            self.accept(k + '-up', self.key, [k, False])

    def ignore_keyboard(self):
        for k in self.keys:
            self.ignore(k)
            self.ignore(k + '-up')
            self.keys[k] = False

    def close_pause_menu(self):
        # TODO: undo show pause menu
        pass

    def show_pause_menu(self):
        # TODO: show a pause menu
        # disable movement / looking
        # show mouse
        pass

    def key(self, key, down):
        self.keys[key] = down

    def start_lookAround(self):
        if self.mouse.hasMouse():
            mouse_pos = Point2(self.mouse.getMouse())
            self.lookAround = mouse_pos, self.body.getH(), self.eye.getP()

    def end_lookAround(self):
        self.lookAround = None

    def recenterMouse(self):
        self.window.movePointer(0,
              int(self.window.getProperties().getXSize() / 2),
              int(self.window.getProperties().getYSize() / 2))

    def move_camera(self, task):
        self.panning = any(self.keys.values())

        dt = globalClock.getDt()
        verticle_move_speed = 75
        horizontal_move_speed = 75
        if self.keys['w']:
            self.body.setY(self.body, dt * horizontal_move_speed)
        if self.keys['s']:
            self.body.setY(self.body, -dt * horizontal_move_speed)
        if self.keys['a']:
            self.body.setX(self.body, -dt * horizontal_move_speed)
        if self.keys['d']:
            self.body.setX(self.body, dt * horizontal_move_speed)
        if self.keys['space']:
            self.body.setZ(self.body, dt * verticle_move_speed)
        if self.keys['lshift']:
            self.body.setZ(self.body, -dt * verticle_move_speed)

        if self.panning:
            pos = self.body.getPos()
            self.body.setPos(bound(pos.x, 0, self.extents.x),
                             bound(pos.y, 0, self.extents.y),
                             pos.z)

        if self.lookAround:
            if self.mouse.hasMouse():
                end = self.mouse.getMouse()

                if self.lookAround:
                    start, h, p = self.lookAround
                    self.body.setH(h + (start.x - end.x) * 50)
                    self.eye.setP(bound(p - (start.y - end.y) * 50, -90, 45))



        return task.cont
