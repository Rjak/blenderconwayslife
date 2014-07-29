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


class Simulation(object):
    """Computes the lives and deaths of lifeforms at each generation."""

    def __init__(self, universe):
        self.universe = universe
        self.generation = 0
        self.births = 0
        self.deaths = 0

    def advance(self):
        """Walks the universe in a O(2n) traversal and advances to the next
        generation.
        """
        self.generation += 1
        self.births = 0
        self.deaths = 0
        for lf in self.universe:
            nbs = self.universe.get_neighbour_count(lf)
            if lf.is_alive():
                if nbs < 2:
                    lf.kill(self.generation)
                    self.deaths += 1
                elif nbs > 3:
                    lf.kill(self.generation)
                    self.deaths += 1
            else:
                if nbs == 3:
                    lf.birth(self.generation)
                    self.births += 1
        self.__commit()

    def __commit(self):
        """Performs a O(n) traversal which updates all LifeForms to the new
          state which was previously computed during a simulation advancement
          pass.
        """
        for x in range(0, self.universe.rows):
            for y in range(0, self.universe.cols):
                lf = self.universe.get_life_form(x, y)
                lf.commit()
