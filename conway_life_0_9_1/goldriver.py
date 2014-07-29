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
import random
import time

try:
    from golview.blenderrenderer import BlenderRenderer
except ImportError:
    print("cannot import BlenderRenderer in this context")

from golview.consolerenderer import ConsoleRenderer
from golcontrol.simulation import Simulation
from golmodel.universe import Universe


class GOLDriver(object):
    """Main driver class that sets up a Game Of Life simulation"""

    DEFAULT_CFG_PATH = "%s%sgolconfig.cfg" % (os.path.dirname(__file__), os.sep)
    FRAME_DELAY = 0.0417    # for 24fps

    def __init__(self, cfg_path=DEFAULT_CFG_PATH):
        """:param cfg_path: the path to a config file that specifies all the
          simulation settings
        """
        self._cfg = GOLDriver.load_config(cfg_path)
        self.__preinit()
        self._generation_count = self._cfg.getint('Universe', 'GenerationCount')
        val = self._cfg.getint('Universe', 'Size')
        self._universe = Universe(val, val)
        self._sim = Simulation(self._universe)
        self._renderer = self.create_renderer()

    def __preinit(self):
        """Initialization tasks which *must* be performed before anything else.
        """
        if self._cfg.has_option('Universe', 'RandomSeed'):
            random.seed(self._cfg.get('Universe', 'RandomSeed'))

    @staticmethod
    def load_config(cfg_path=DEFAULT_CFG_PATH):
        """Loads the config file at the specified path.

        :param cfg_path: complete path to a config file containing all the
          settings for the simulation
        """
        cfg = configparser.RawConfigParser()
        cfg.read_file(open(cfg_path))  # confirm file exists
        cfg.read(cfg_path)
        return cfg

    def create_renderer(self):
        """Factory method which instantiates the correct renderer specified
        by the config file.
        """
        rtype = self._cfg.get('Rendering', 'Renderer')
        if rtype == "console":
            return ConsoleRenderer()
        elif rtype == "blender":
            return BlenderRenderer(self._universe)
        else:
            raise Exception("unsupported renderer '%r'" % rtype)

    def sim_loop(self):
        """Runs the simulation."""
        frame_delay = self._renderer.get_frame_delay()

        for i in range(0, self._generation_count):
            self._sim.advance()
            print("\ngeneration %d  -  births: %d  -  deaths: %d" %
                  (i, self._sim.births, self._sim.deaths))
            self._renderer.render(self._universe)
            if frame_delay > 0.0:
                time.sleep(frame_delay)

        cnt = self._universe.get_transition_count()
        print("total transitions: ", cnt)

    def go(self):
        """Performs all setup and then runs the simulation"""
        self._universe.randomize()
        self._renderer.render(self._universe)
        time.sleep(self._cfg.getint('Rendering', 'PauseAfterRandomize'))
        self.sim_loop()
