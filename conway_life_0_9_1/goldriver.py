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

    DEFAULT_CFG_NAME = "%s%sgolconfig.cfg" % (os.path.dirname(__file__), os.sep)
    FRAME_DELAY = 0.0417    # for 24fps

    def __init__(self, cfg_name = DEFAULT_CFG_NAME):
        self._cfg = self._load_config(cfg_name)
        self._generation_count = self._cfg.getint('Universe', 'GenerationCount')
        val = self._cfg.getint('Universe', 'Size')
        self._universe = Universe(val, val)
        self._sim = Simulation(self._universe)
        self._renderer = self._create_renderer() 

    def _load_config(self, cfg_name = DEFAULT_CFG_NAME):
        cfg = configparser.RawConfigParser()
        cfg.readfp(open(cfg_name)) # confirm file exists
        cfg.read(cfg_name)
        return cfg

    def _create_renderer(self):
        rtype = self._cfg.get('Rendering', 'Renderer')
        if rtype == "console":
            return ConsoleRenderer()
        elif rtype == "blender":
            return BlenderRenderer(self._universe)
        else:
            raise Exception("unsupported renderer '%r'" % rtype)

    def _sim_loop(self):
        oldBirths = 0
        oldDeaths = 0
        frameDelay = self._renderer.get_frame_delay()

        for i in range (0, self._generation_count):
            self._sim.advance()
            print("\ngeneration %d  -  births: %d  -  deaths: %d" % \
              (i, self._sim.births, self._sim.deaths))
            oldBirths = self._sim.births
            oldDeaths = self._sim.deaths
            self._renderer.render(self._universe)
            if frameDelay > 0.0:
                time.sleep(frameDelay)

        cnt = self._universe.get_transition_count()
        print("total transitions: ", cnt)

    def go(self):
        self._universe.randomize()
        self._renderer.render(self._universe)
        time.sleep(self._cfg.getint('Rendering', 'PauseAfterRandomize'))
        self._sim_loop()
