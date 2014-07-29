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
import random

from golmodel.lifeform import LifeForm


class Universe(object):
    """A 'Universe' is an iterable, 2D grid of LifeForm objects. When iterating
    over the universe, lifeforms are yielded in row-major form (so every
    LifeForm in row 0 is returned, followed by every LifeForm in row 1, etc).
    """

    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.lifeform_count = rows * cols
        self.lifeforms = []         # 1D list representation of 2D grid
        self.__make_universe()

    def __iter__(self):
        return iter(self.lifeforms)

    def __make_universe(self):
        """Instantiates all the LifeForm objects in the Universe."""
        for i in range(self.lifeform_count):
            # 'simulate' 2D grid with math
            row = i // self.cols
            col = i % self.cols
            self.lifeforms.append(LifeForm(i, row, col))

    def randomize(self, thresh=0.4, do_kills=True):
        """Randomly kill or birth life forms in the universe.

        :param thresh: normalized floating threshold that describes the
          likelihood that each cell will be alive rather than dead
        :param do_kills: if True, LifeForms that we randomly selected for death
          will be killed, otherwise they are left alone (used to randomly
          rebirth a portion of the population rather than a complete reset)
        """
        for lf in self:
            if random.random() > thresh:
                if do_kills:
                    lf.kill(0)
            else:
                lf.birth(0)
            lf.commit()

    def get_life_form(self, row, col):
        """Gets the LifeForm at the given position in the grid.

        :param row: desired LifeForm's row
        :param col: desired LifeForm's column
        :return: the LifeForm at row x column
        """
        index = (row * self.cols) + col
        return self.lifeforms[index]

    def get_neighbour_count(self, lf):
        """Gets the living neighbour count for the box surrounding the given
        LifeForm.

        :param lf: the LifeForm whose neighbour count is desired
        """
        cnt = 0
        if lf.row > 0:
            cnt += self.__get_neighbour_count_for_row(lf.row - 1, lf.col)
        cnt += self.__get_neighbour_count_for_row(lf.row, lf.col, True)
        if lf.row < self.rows - 1:
            cnt += self.__get_neighbour_count_for_row(lf.row + 1, lf.col)
        return cnt

    def __get_neighbour_count_for_row(self, row, col, is_home=False):
        """Gets the neighbour count for the given row and surrounding columns.
        If is_home is true, then the center column is not considered.

        :param row: the desired row of analysis
        :param col: the desired column of analysis
        :param is_home: if True, the column is not counted as a neighbour
        :return: neighbour count for the given row and column
        """
        cnt = 0
        if col > 0:
            if self.get_life_form(row, col - 1).is_alive():
                cnt += 1
        if (is_home is False) and self.get_life_form(row, col).is_alive():
            cnt += 1
        if col < self.cols - 1:
            if self.get_life_form(row, col + 1).is_alive():
                cnt += 1
        return cnt

    def get_transition_count(self):
        """Gets the total count of life/death transitions that have occurred
          during the lifetime of the universe.

        :return: the total number of life/death transitions that have occurred
          so far in the simulation
        """
        total = 0
        for lf in self:
            print("%d: %d %s" % (lf.lfid, len(lf.transitions),
                                 lf.transitions_to_string()))
            total += lf.get_transition_count()
        return total

    def __repr__(self):
        selfname = self.__class__.__name__
        return "{}[rows={}, cols={}, lf_count={}]".format(selfname, self.rows,
                                                          self.cols,
                                                          self.lifeform_count)
