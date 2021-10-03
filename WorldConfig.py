import random

from panda3d.core import Vec3
from panda3d.core import BitMask32
from panda3d.core import Shader, ShaderAttrib
from panda3d.core import PointLight
from panda3d.core import AntialiasAttrib

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletPlaneShape

# Class of the Physics world!!
# add and remove objects

import ObjectPhysics


class World():
    def __init__(self, taskMgr, render, loader):

        self.taskMgr = taskMgr
        self.render = render

        self.world = BulletWorld()
        self.world.set_gravity(Vec3(0, 0, -9.81))

        arena_1 = loader.load_model('media/models/area.gltf')
        arena_1.reparent_to(self.render)
        arena_1.set_pos(0, 0, 0)

        # Turn arena solid
        self.make_collision_from_model(arena_1, 0, 0, self.world, (arena_1.get_pos()))

        # Create light points
        self.generatePointLight()

        # Generate Shaders
        self.generateShader()

        # infinite ground plane
        # the world-Z limit
        ground_plane = BulletPlaneShape(Vec3(0, 0, 1), 0)
        node = BulletRigidBodyNode('ground')
        node.add_shape(ground_plane)
        node.set_friction(0.1)
        np = self.render.attach_new_node(node)
        np.set_pos(0, 0, -1)
        self.world.attach_rigid_body(node)

    def generateShader(self):
        self.scene_shader = Shader.load(Shader.SL_GLSL, "media/shaders/simplepbr_vert_mod_1.vert",
                                                        "media/shaders/simplepbr_frag_mod_1.frag")
        self.render.set_shader(self.scene_shader)
        self.render.set_antialias(AntialiasAttrib.MMultisample)
        self.scene_shader = ShaderAttrib.make(self.scene_shader)
        self.scene_shader = self.scene_shader.setFlag(ShaderAttrib.F_hardware_skinning, True)

    def getShader(self):
        return self.scene_shader

    # Create collision body from input model
    def make_collision_from_model(self, input_model, node_number, mass, world, target_pos):
        # tristrip generation from static models
        # generic tri-strip collision generator begins
        geom_nodes = input_model.find_all_matches('**/+GeomNode')
        geom_nodes = geom_nodes.get_path(node_number).node()
        geom_target = geom_nodes.get_geom(0)
        output_bullet_mesh = BulletTriangleMesh()
        output_bullet_mesh.add_geom(geom_target)
        tri_shape = BulletTriangleMeshShape(output_bullet_mesh, dynamic=False)

        body = BulletRigidBodyNode('input_model_tri_mesh')
        np = self.render.attach_new_node(body)
        np.node().add_shape(tri_shape)
        np.node().set_mass(mass)
        np.node().set_friction(0.01)
        np.set_pos(target_pos)
        np.set_scale(1)
        np.set_collide_mask(BitMask32.allOn())
        world.attach_rigid_body(np.node())

    def generatePointLight(self):
        # point light generator
        for x in range(5):
            plight_1 = PointLight('plight')
            # add plight props here
            plight_1_node = self.render.attach_new_node(plight_1)
            # group the lights close to each other to create a sun effect
            plight_1_node.set_pos(random.uniform(-21, -20), random.uniform(-21, -20), random.uniform(20, 21))
            self.render.set_light(plight_1_node)

        # point light for volumetric lighting filter
        plight_1 = PointLight('plight')
        # add plight props here
        plight_1_node = self.render.attach_new_node(plight_1)
        # group the lights close to each other to create a sun effect
        plight_1_node.set_pos(random.uniform(-21, -20), random.uniform(-21, -20), random.uniform(20, 21))
        self.render.set_light(plight_1_node)

