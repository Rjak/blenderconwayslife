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

from golmodel.lifeform import LifeForm
from golmodel.universe import Universe

from .blenderlifeform import BlenderLifeForm
from .golrenderer import GOLRenderer

class BlenderRenderer(GOLRenderer):
    """Renders mesh instances and keyframes to Blender"""

    BLENDER_CONFIG_FILE = "%s%sblenderrenderer.cfg" % \
      (os.path.dirname(__file__), os.sep)

    def __init__(self, universe):
        print("BLENDER RENDERER")

        self.cfg = self._load_config()

        self._universe = universe
        self._curr_frame = self.cfg.getint('Time', 'StartFrame')

        self.setup()

    def _load_config(self):
        cfg = configparser.RawConfigParser()
        cfg.readfp(open(self.BLENDER_CONFIG_FILE)) # confirm file exists
        cfg.read(self.BLENDER_CONFIG_FILE)
        return cfg

    def setup(self):
        self.blender_life_forms = []
        for lf in self._universe:
            self.blender_life_forms.append(BlenderLifeForm(self.cfg, lf))

    def render(self, universe):
        self._depth_first_render()

    def _depth_first_render(self):
        """
        Depth-first render which only lays down keyframes which a life form's
        state transitions.
        """
        for blf in self.blender_life_forms:
            self._df_render_life_form(blf)

    def _df_render_life_form(self, blf):
        if (len(blf.lifeform.transitions) < 1):
            sys.exit("INVALID: lifeform %s has no transitions" % (blf))
        tr = blf.lifeform.transitions[0]
        currGen = tr[0]
        currState = tr[1]
        blf.update_to_state(currState)
        blf.set_keys(currGen)

        first = True

        for tr in blf.lifeform.transitions:
            if (first):
                first = False
                continue
            currGen = tr[0]
            currState = tr[1]
            blf.set_keys(currGen - 1)
            blf.update_to_state(currState)
            blf.set_keys(currGen)

    def _breadth_first_render(self, universe):
        """
        Brute force render which lays down a keyframe for every lifeform at
        every generation, which is extremely wasteful. This method is left in
        for discussion.
        """
        print("setting simulation keys for frame: %d" % (self._curr_frame))
        bpy.context.scene.frame_set(self._curr_frame)
        for blf in self.blender_life_forms:
            blf.update()
            blf.set_keys(self._curr_frame)
        self._curr_frame += 1
