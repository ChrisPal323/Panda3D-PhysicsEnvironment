from panda3d.core import Vec3, Point2, LVecBase3f, BitMask32
from direct.showbase.ShowBase import ShowBase

from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape

import numpy as np


# Object configs
# name - String
# pos - (x, y, z)
# shape - Vec3
# mass - float
# friction - float
# modelPath - String
# Color - (r, g, b, a)

class Object():
    def __init__(self, render, world, loader, name, pos, shape, mass, friction, modelPath, color):

        # Attributes
        self.render = render
        self.world = world
        self.loader = loader

        # Dynamic Collision
        special_shape = BulletBoxShape(shape)

        # Rigid-body
        body = BulletRigidBodyNode(name)
        d_coll = self.render.attach_new_node(body)
        d_coll.node().add_shape(special_shape)
        d_coll.node().set_mass(mass)
        d_coll.node().set_friction(friction)
        d_coll.set_collide_mask(BitMask32.allOn())

        # turn on Continuous Collision Detection
        d_coll.node().set_ccd_motion_threshold(1e-7)
        d_coll.node().set_ccd_swept_sphere_radius(0.30)
        d_coll.node().set_deactivation_enabled(False)
        d_coll.set_pos(pos)
        box_model = self.loader.load_model(modelPath)
        box_model.reparent_to(self.render)
        box_model.reparent_to(d_coll)
        box_model.set_color(color)
        self.world.attach_rigid_body(d_coll.node())
