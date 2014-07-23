from golmodel.lifeform import LifeForm
from golmodel.universe import Universe

from .golrenderer import GOLRenderer

class ConsoleRenderer(GOLRenderer):
    """Renders the simulation to stdout"""

    FRAME_DELAY = 0.0417 # for 24fps
    ALIVE_CHAR = "*"
    DEAD_CHAR = " "

    def __init__(self):
        print("CONSOLE RENDERER")

    def render(self, universe):
        for x in range (0, universe.rows):
            row = ""
            for y in range (0, universe.cols):
                lf = universe.get_life_form(x, y)
                if lf.state == lf.STATE_ALIVE:
                    row += self.ALIVE_CHAR
                elif lf.state == lf.STATE_DEAD:
                    row += self.DEAD_CHAR
                row += " "
            print(row)
    
    def get_frame_delay(self):
        return self.FRAME_DELAY
