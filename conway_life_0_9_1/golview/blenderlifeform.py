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

    # Blender requires a 20-element tuple to dictate which layers an object
    # should be visible on
    CELL_LAYER		= 3

    LIGHT_PRE		= "LightPlane_"
    CELL_PRE		= "Cell_"
    LIGHT_MAT_SUFF         = "_PlaneMat"

    def __init__(self, cfg, lifeForm):
        self.cfg = cfg

        self._set_config_values()

        self._cell_layers = [False] * 20
        self._cell_layers[self.CELL_LAYER] = True
        self._emission_node = None
        self._lf = lifeForm
        self._light_obj_name = "%s%d" % (self.LIGHT_PRE, self._lf.lfid)
        self._cell_obj_name = "%s%d" % (self.CELL_PRE, self._lf.lfid)
        self._was_alive = self._lf.is_alive()
        self._light_mesh = None
        self._light_obj = None
        self._plane_mat = None
        self._cell_obj = None

        self.setup()
        self._realize_plane()
        self._realize_cell()
        self.update()

    @property
    def lifeform(self):
        return self._lf

    def _set_config_values(self):
        val = self.cfg.getfloat('CellLight', 'DeadSize')
        self.deadSizeVector = (val, val, val)

        val = self.cfg.getfloat('CellLight', 'AliveSize')
        self.aliveSizeVector = (val, val, val)

        self.cellSz = self.cfg.getfloat('CellCage', 'CellSize')
        self.cellCageSz = self.cfg.getfloat('CellCage', 'Size') 
        self.cellCagePad = self.cfg.getfloat('CellCage', 'Pad') 
        val = self.cfg.getfloat('CellCage', 'LightSizeCoefficient')
        self.cellCageLightSz = self.cellCageSz - (val * self.cellCagePad)
        self.cellXInCage = self.cfg.getfloat('CellCage', 'CellX')
        self.cellYInCage = self.cfg.getfloat('CellCage', 'CellY')

        self.deadStrength = self.cfg.getfloat('CellLight', 'DeadStrength') 
        self.deadSize = self.cfg.getfloat('CellLight', 'DeadSize') 
        self.aliveStrength = self.cfg.getfloat('CellLight', 'AliveStrength') 
        self.aliveSize = self.cfg.getfloat('CellLight', 'AliveSize') 

        self.lightsZPlane = self.cfg.getfloat('MeshSetup', 'LightsZPlane') 
        self.cellsZPlane = self.cfg.getfloat('MeshSetup', 'CellsZPlane') 

    def setup(self):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['OriginalCell'].select = True
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        bpy.ops.object.select_all(action='DESELECT')

    def _realize_plane(self):
        x = (self._lf.col * self.cellCageSz) + self.cellCagePad
        y = (self._lf.row * self.cellCageSz) + self.cellCagePad
        z = self.lightsZPlane
        vert0 = (x, y, z)
        vert1 = (x, y + self.cellCageLightSz, z)
        vert2 = (x + self.cellCageLightSz, y + self.cellCageLightSz, z)
        vert3 = (x + self.cellCageLightSz, y , z)
        verts = [vert0, vert1, vert2, vert3] 
        faces = [(0, 1, 2, 3)]

        self._light_mesh = bpy.data.meshes.new("Plane")
        self._light_obj = bpy.data.objects.new(self._light_obj_name, \
          self._light_mesh)
        bpy.context.scene.objects.link(self._light_obj)
        self._light_mesh.from_pydata(verts, [], faces)
        self._light_mesh.update(calc_edges=True)
        name = "%d%s" % (self._lf.lfid, self.LIGHT_MAT_SUFF)
        self._init_plane_material(name)
        self._light_obj.data.materials.append(self._plane_mat)
        self._light_obj.cycles_visibility.camera = False
        self._select_light_object()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        bpy.ops.object.select_all(action='DESELECT')

    def _realize_cell(self):
        x = self._lf.col * self.cellCageSz
        y = self._lf.row * self.cellCageSz
        z = self.cellsZPlane
        loc = (x + self.cellXInCage, y + self.cellYInCage, z)
        rot = (random.randrange(0, 359), random.randrange(0, 359), \
          random.randrange(0, 359))
        rotaxis = (random.randrange(0, 1), random.randrange(0, 1), \
          random.randrange(0, 1))
        rotamt = random.randrange(0, 359)

        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['OriginalCell'].select = True
        bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
        bpy.data.objects['OriginalCell'].select = True
        self._cell_obj = self._duplicate_cell(self._cell_obj_name, \
          bpy.context.object)
        bpy.context.scene.objects.link(self._cell_obj)
        self._cell_obj.location = loc
        self._cell_obj.delta_rotation_euler = rot
        self._cell_obj.layers = self._cell_layers

    def _duplicate_cell(self, name, copyobj):
        mesh = bpy.data.meshes.new(name)
        obNew = bpy.data.objects.new(name, mesh)
        obNew.data = copyobj.data.copy()
        obNew.scale = copyobj.scale
        obNew.location = copyobj.location
        return (obNew)

    def _realize_sphere(self):
        x = self._lf.col * self.cellCageSz
        y = self._lf.row * self.cellCageSz
        z = self.cellsZPlane
        loc = (x + self.cellXInCage, y + self.cellXInCage, z)
        bpy.ops.mesh.primitive_uv_sphere_add(size = self.cellSz / 2, \
          location=loc)

    def _init_plane_material(self, name):
        self._plane_mat = bpy.data.materials.new(name)
        self._plane_mat.use_nodes = True
        surf_node = self._plane_mat.node_tree.nodes[0]
        self._emission_node = self._plane_mat.node_tree.nodes.new( \
          "ShaderNodeEmission")
        self._emission_node.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
        self._emission_node.inputs['Strength'].default_value = \
          self.deadStrength
        outputSocket = self._emission_node.outputs["Emission"]
        inputSocket = surf_node.inputs["Surface"]
        self._plane_mat.node_tree.links.new(outputSocket, inputSocket)

    def _select_light_object(self):
        bpy.ops.object.select_all(action = 'DESELECT')
        bpy.ops.object.select_pattern(pattern = self._light_obj_name)

    def _set_alive(self):
        self._set_strength(self.aliveStrength)
        self._light_obj.scale = self.aliveSizeVector

    def _set_dead(self):
        self._set_strength(self.deadStrength)
        self._light_obj.scale = self.deadSizeVector

    def _set_strength(self, strength):
        self._emission_node.inputs['Strength'].default_value = strength

    def update_to_state(self, state):
        if (state == self._lf.STATE_ALIVE):
            self._set_alive()
        elif (state == self._lf.STATE_DEAD):
            self._set_dead()

    def update(self):
        if (self._lf.is_alive()):
            self._set_alive()
        else:
            self._set_dead()
        self._was_alive = self._lf.is_alive()

    def set_keys(self, currFrame):
        self._emission_node.inputs['Strength'].keyframe_insert( \
          data_path="default_value", frame=currFrame)
        self._light_obj.keyframe_insert('scale', frame=currFrame)

    def __repr__(self):
        return "{}[{}]".format(self.__class__.__name__, self._lf)
