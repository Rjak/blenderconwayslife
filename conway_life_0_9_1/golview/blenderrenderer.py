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
import configparser
import os
import sys

from .blenderlifeform import BlenderLifeForm
from .golrenderer import GOLRenderer


class BlenderRenderer(GOLRenderer):
    """Renders mesh instances and keyframes to Blender"""

    BLENDER_CONFIG_FILE = "%s%sblenderrenderer.cfg" %\
                          (os.path.dirname(__file__), os.sep)

    def __init__(self, universe):
        """:param universe: the Conway universe object"""
        print("BLENDER RENDERER")

        self.cfg = self.__load_config()

        self.universe = universe
        self.curr_frame = self.cfg.getint('Time', 'StartFrame')

        self.__setup()

    @classmethod
    def __load_config(cls):
        """Load settings from the config file."""
        cfg = configparser.RawConfigParser()
        cfg.read_file(open(cls.BLENDER_CONFIG_FILE))  # confirm file exists
        cfg.read(cls.BLENDER_CONFIG_FILE)
        return cfg

    def __setup(self):
        """Simple initialization tasks."""
        self.blender_life_forms = []
        BlenderRenderer.set_origin_geometry_for_original()
        BlenderLifeForm.set_config_values(self.cfg)
        for lf in self.universe:
            self.blender_life_forms.append(BlenderLifeForm(lf))

    @staticmethod
    def set_origin_geometry_for_original():
        """Ensures that the origin for the OriginalCell object in Blender is
        set to geometry origin.
        """
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['OriginalCell'].select = True
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        bpy.ops.object.select_all(action='DESELECT')

    def render(self, universe):
        """Performs a render of the simulation that sets all the keyframes to
        make a beautiful Conway animation.

        :param universe: the Conway universe object
        """
        self.depth_first_render()

    def depth_first_render(self):
        """Depth-first render which only lays down keyframes which a life form's
        state transitions.
        """
        for blf in self.blender_life_forms:
            BlenderRenderer.df_render_life_form(blf)

    @staticmethod
    def df_render_life_form(blf):
        """Walks through the transition vector for the life form and sets the
        keyframes required to render its states through the simulation.

        :param blf: the BlenderLifeForm to render
        """
        if len(blf.lifeform.transitions) < 1:
            sys.exit("INVALID: lifeform %s has no transitions" % blf)
        tr = blf.lifeform.transitions[0]
        curr_gen = tr[0]
        curr_state = tr[1]
        blf.update_to_state(curr_state)
        blf.set_keys(curr_gen)
        first = True

        for tr in blf.lifeform.transitions:
            if first:
                first = False
                continue
            curr_gen = tr[0]
            curr_state = tr[1]
            blf.set_keys(curr_gen - 1)
            blf.update_to_state(curr_state)
            blf.set_keys(curr_gen)

    def breadth_first_render(self):
        """Brute force render which lays down a keyframe for every lifeform at
        every generation, which is extremely wasteful. This method is left in
        for discussion.
        """
        print("setting simulation keys for frame: %d" % self.curr_frame)
        bpy.context.scene.frame_set(self.curr_frame)
        for blf in self.blender_life_forms:
            blf.__update()
            blf.set_keys(self.curr_frame)
        self.curr_frame += 1
