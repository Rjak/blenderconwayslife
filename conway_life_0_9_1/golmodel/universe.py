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
import math
import random

from golmodel.lifeform import LifeForm

class Universe(object):
    """
    A 'Universe' is an iterable, 2D grid of LifeForm objects. When iterating
    over the universe, lifeforms are yielded in row-major form (so every
    LifeForm in row 0 is returned, followed by every LifeForm in row 1, etc).
    """

    def __init__(self, rows = 10, cols = 10):
        self._rows = rows
        self._cols = cols
        self._lf_count = rows * cols
        self._life_forms = []         # 1D list representation of 2D grid
        self._make_universe()

    def __iter__(self):
        return iter(self._life_forms)

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    def _make_universe(self):
        """Instantiates all the LifeForm objects in the Universe."""
        for i in range(self._lf_count):
            # 'simulate' 2D grid with math
            row = i // self._cols
            col = i % self._cols
            self._life_forms.append(LifeForm(i, row, col))

    def randomize(self, thresh = 0.4, doKills = True):
        """Randomly kill or birth life forms in the universe."""
        for lf in self:
            if random.random() > thresh:
                if doKills:
                    lf.kill(0)
            else:
                lf.birth(0)
            lf.commit()

    def get_life_form(self, row, col):
        """Returns the life form at row, col."""
        index = (row * self._cols) + col
        return self._life_forms[index]

    def get_neighbour_count(self, lf):
        """
        Returns the living neighbour count for the box surrounding the given
        life form.
        """
        cnt = 0
        if lf.row > 0:
            cnt += self.get_neighbour_count_for_row(lf.row - 1, lf.col)
        cnt += self.get_neighbour_count_for_row(lf.row, lf.col, True)
        if lf.row < self._rows - 1:
            cnt += self.get_neighbour_count_for_row(lf.row + 1, lf.col)
        return cnt

    def get_neighbour_count_for_row(self, row, col, is_home = False):
        """
        Returns the neighbour count for the given row and surrounding columns.
        If is_home is true, then the center column is not considered.
        """
        cnt = 0
        if col > 0:
            if self.get_life_form(row, col - 1).is_alive():
                cnt += 1
        if (is_home == False) and self.get_life_form(row, col).is_alive():
            cnt += 1
        if col < self._cols - 1:
            if self.get_life_form(row, col + 1).is_alive():
                cnt += 1
        return cnt

    def get_transition_count(self):
        """
        Returns the total count of life/death transitions that have occurred
        during the lifetime of the universe.
        """
        total = 0
        for lf in self:
            print("%d: %d %s" % (lf.lfid, len(lf.transitions), \
              lf.transitions_to_string()))
            total += lf.get_transition_count()
        return total

    def __repr__(self):
        return "{}[rows={}, cols={}, lf_count={}]".format( \
          self.__class__.__name__, self._rows, self._cols, self._lf_count)
