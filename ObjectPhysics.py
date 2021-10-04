from panda3d.core import Vec3, Point2, LVecBase3f, BitMask32
from direct.showbase.ShowBase import ShowBase

from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape, BulletSphereShape

import numpy as np


# Box configs
# name - String
# pos - (x, y, z)
# shape - Vec3
# mass - float
# friction - float
# modelPath - String
# Color - (r, g, b, a)
class BoxObject():
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
        model = self.loader.load_model(modelPath)
        model.reparent_to(self.render)
        model.setSx(shape[0])
        model.setSy(shape[1])
        model.setSz(shape[2])
        model.reparent_to(d_coll)
        model.set_color(color)
        self.world.attach_rigid_body(d_coll.node())


# Object configs
# name - String
# pos - (x, y, z)
# radius - float
# mass - float
# friction - float
# modelPath - String
# Color - (r, g, b, a)
class BallObject():
    def __init__(self, render, world, loader, name, pos, radius, mass, friction, modelPath, color):

        # Attributes
        self.render = render
        self.world = world
        self.loader = loader

        # Dynamic Collision
        special_shape = BulletSphereShape(radius)

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
        model = self.loader.load_model(modelPath)
        model.setScale(radius)  # Since model is 1m we can scale using size directly
        model.reparent_to(self.render)
        model.reparent_to(d_coll)
        model.set_color(color)
        self.world.attach_rigid_body(d_coll.node())
