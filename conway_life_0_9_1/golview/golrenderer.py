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
import abc


class GOLRenderer(object):
    """Game of Life Renderer Base Class"""

    @abc.abstractmethod
    def render(self, universe):
        """Called by the driver to render one generation of the sim"""
        raise NotImplementedError
    
    def get_frame_delay(self):
        """Optional simulation delay to prevent the simulation from running too
        fast to be visible.
        """
        return 0
