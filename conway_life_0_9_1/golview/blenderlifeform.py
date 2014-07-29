# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
import bpy
import random


class BlenderLifeForm(object):
    """Wraps a standard golmodel.lifeform.LifeForm in a class that knows how to
    visually represent a LifeForm in Blender.
    """

    # Blender requires a 20-element tuple of booleans to describe which layer
    # to place objects on.
    CELL_LAYER = 3

    LIGHT_PRE = "LightPlane_"
    CELL_PRE = "Cell_"
    LIGHT_MAT_SUFF = "_PlaneMat"

    def __init__(self, lf):
        """:param lf: the LifeForm to wrap"""

        self.cell_layers = [False] * 20
        self.cell_layers[self.CELL_LAYER] = True
        self.emission_node = None
        self.lf = lf
        self.light_obj_name = "%s%d" % (self.LIGHT_PRE, self.lf.lfid)
        self.cell_obj_name = "%s%d" % (self.CELL_PRE, self.lf.lfid)
        self.was_alive = self.lf.is_alive()
        self.light_mesh = None
        self.light_obj = None
        self.plane_mat = None
        self.cell_obj = None

        self.__realize_plane()
        self.__realize_cell()
        self.__update()

    @classmethod
    def set_config_values(cls, cfg):
        """Pull configuration values into the object from the config file.

        :param cfg: config object which carries visual settings (see README.md)
        """
        val = cfg.getfloat('CellLight', 'DeadSize')
        cls.deadSizeVector = (val, val, val)

        val = cfg.getfloat('CellLight', 'AliveSize')
        cls.aliveSizeVector = (val, val, val)

        cls.cellSz = cfg.getfloat('CellCage', 'CellSize')
        cls.cellCageSz = cfg.getfloat('CellCage', 'Size')
        cls.cellCagePad = cfg.getfloat('CellCage', 'Pad')
        val = cfg.getfloat('CellCage', 'LightSizeCoefficient')
        cls.cellCageLightSz = cls.cellCageSz - (val * cls.cellCagePad)
        cls.cellXInCage = cfg.getfloat('CellCage', 'CellX')
        cls.cellYInCage = cfg.getfloat('CellCage', 'CellY')

        cls.deadStrength = cfg.getfloat('CellLight', 'DeadStrength')
        cls.deadSize = cfg.getfloat('CellLight', 'DeadSize')
        cls.aliveStrength = cfg.getfloat('CellLight', 'AliveStrength')
        cls.aliveSize = cfg.getfloat('CellLight', 'AliveSize')

        cls.lightsZPlane = cfg.getfloat('MeshSetup', 'LightsZPlane')
        cls.cellsZPlane = cfg.getfloat('MeshSetup', 'CellsZPlane')

    def __realize_plane(self):
        """Creates a new plane object, positioned above the LifeForm which is
        emissive and serve to light the LifeForm.
        """
        x = (self.lf.col * self.cellCageSz) + self.cellCagePad
        y = (self.lf.row * self.cellCageSz) + self.cellCagePad
        z = self.lightsZPlane
        vert0 = (x, y, z)
        vert1 = (x, y + self.cellCageLightSz, z)
        vert2 = (x + self.cellCageLightSz, y + self.cellCageLightSz, z)
        vert3 = (x + self.cellCageLightSz, y, z)
        verts = [vert0, vert1, vert2, vert3] 
        faces = [(0, 1, 2, 3)]

        self.light_mesh = bpy.data.meshes.new("Plane")
        self.light_obj = bpy.data.objects.new(self.light_obj_name,
                                              self.light_mesh)
        bpy.context.scene.objects.link(self.light_obj)
        self.light_mesh.from_pydata(verts, [], faces)
        self.light_mesh.__update(calc_edges=True)
        name = "%d%s" % (self.lf.lfid, self.LIGHT_MAT_SUFF)
        self.__init_plane_material(name)
        self.light_obj.data.materials.append(self.plane_mat)
        self.light_obj.cycles_visibility.camera = False
        self.__select_light_object()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        bpy.ops.object.select_all(action='DESELECT')

    def __realize_cell(self):
        """Creates a new instance of the OriginalCell at the correct position
        in 3-space.
        """
        x = self.lf.col * self.cellCageSz
        y = self.lf.row * self.cellCageSz
        z = self.cellsZPlane
        loc = (x + self.cellXInCage, y + self.cellYInCage, z)
        rot = (random.randrange(0, 359), random.randrange(0, 359),
               random.randrange(0, 359))

        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['OriginalCell'].select = True
        bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
        bpy.data.objects['OriginalCell'].select = True
        self.cell_obj = self.__duplicate_cell(self.cell_obj_name,
                                              bpy.context.object)
        bpy.context.scene.objects.link(self.cell_obj)
        self.cell_obj.location = loc
        self.cell_obj.delta_rotation_euler = rot
        self.cell_obj.layers = self.cell_layers

    @staticmethod
    def __duplicate_cell(name, object_to_copy):
        """Performs the actual work of creating a new instance of the given
        object.

        :param name: the name to assign to the new instance
        :param object_to_copy: the object to copy
        """
        mesh = bpy.data.meshes.new(name)
        ob_new = bpy.data.objects.new(name, mesh)
        ob_new.data = object_to_copy.data.copy()
        ob_new.scale = object_to_copy.scale
        ob_new.location = object_to_copy.location
        return ob_new

    def __realize_sphere(self):
        """Can replace __duplicate_cell() to simply create spheres for LifeForms
        rather than mesh instances.
        """
        x = self.lf.col * self.cellCageSz
        y = self.lf.row * self.cellCageSz
        z = self.cellsZPlane
        loc = (x + self.cellXInCage, y + self.cellXInCage, z)
        bpy.ops.mesh.primitive_uv_sphere_add(size=self.cellSz / 2, location=loc)

    def __init_plane_material(self, name):
        """Initializes the emissive plane material which serves to light the
        LifeForm.
        """
        self.plane_mat = bpy.data.materials.new(name)
        self.plane_mat.use_nodes = True
        surf_node = self.plane_mat.node_tree.nodes[0]
        self.emission_node = self.plane_mat.node_tree.nodes.new(
            "ShaderNodeEmission")
        self.emission_node.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
        self.emission_node.inputs['Strength'].default_value = self.deadStrength
        output_socket = self.emission_node.outputs["Emission"]
        input_socket = surf_node.inputs["Surface"]
        self.plane_mat.node_tree.links.new(output_socket, input_socket)

    def __select_light_object(self):
        """Selects the plane which serves to light the LifeForm."""
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_pattern(pattern=self.light_obj_name)

    def __set_alive(self):
        """Sets values which visually indicate the LifeForm has been birthed."""
        self.__set_strength(self.aliveStrength)
        self.light_obj.scale = self.aliveSizeVector

    def __set_dead(self):
        """Sets values which visually indicate the LifeForm has died."""
        self.__set_strength(self.deadStrength)
        self.light_obj.scale = self.deadSizeVector

    def __set_strength(self, strength):
        """Logically encapsulates the notion of setting a light strength.

        :param strength: a normalized floating point value indicating the
          strength of the light
        """
        self.emission_node.inputs['Strength'].default_value = strength

    def update_to_state(self, state):
        """Visually updates the LifeForm to be either alive or dead.

        :param state: one of golmodel.lifeform.LifeForm.STATE_ALIVE or
          golmodel.lifeform.LifeForm.STATE_DEAD
        """
        if state == self.lf.STATE_ALIVE:
            self.__set_alive()
        elif state == self.lf.STATE_DEAD:
            self.__set_dead()

    def __update(self):
        """Updates internal flags which allow us to determine whether the state
        of the LifeForm has changed since the previous generation.
        """
        if self.lf.is_alive():
            self.__set_alive()
        else:
            self.__set_dead()
        self.was_alive = self.lf.is_alive()

    def set_keys(self, curr_frame):
        """Adds all keyframes required to visually present the correct state of
        the LifeForm at the given keyframe.

        :param curr_frame: the frame at which to set the keyframes
        """
        self.emission_node.inputs['Strength'].\
            keyframe_insert(data_path="default_value", frame=curr_frame)
        self.light_obj.keyframe_insert('scale', frame=curr_frame)

    def __repr__(self):
        return "{}[{}]".format(self.__class__.__name__, self.lf)
