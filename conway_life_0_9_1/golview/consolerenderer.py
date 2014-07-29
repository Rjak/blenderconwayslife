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

from .golrenderer import GOLRenderer


class ConsoleRenderer(GOLRenderer):
    """Renders the simulation to stdout"""

    FRAME_DELAY = 0.0417  # for 24fps
    ALIVE_CHAR = "*"
    DEAD_CHAR = " "

    def __init__(self):
        print("CONSOLE RENDERER")

    def render(self, universe):
        """Renders the simulation to the console.

        :param universe: the Conway universe object
        """
        for x in range(0, universe.rows):
            row = ""
            for y in range(0, universe.cols):
                lf = universe.get_life_form(x, y)
                if lf.state == lf.STATE_ALIVE:
                    row += self.ALIVE_CHAR
                elif lf.state == lf.STATE_DEAD:
                    row += self.DEAD_CHAR
                row += " "
            print(row)
    
    def get_frame_delay(self):
        """Override the simulation delay so that it does not go by so fast that
        it cannot be observed.
        """
        return self.FRAME_DELAY
