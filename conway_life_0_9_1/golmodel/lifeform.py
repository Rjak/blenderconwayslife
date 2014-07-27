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

class LifeForm(object):
    """Lifeform model object for Life simulation."""

    def __init__(self, lfid = 0, row = 0, col = 0):
        self.STATE_NONE		= -1
        self.STATE_DEAD		= 0
        self.STATE_ALIVE	= 1

        self.transitions = []
        self.state = self.STATE_NONE
        self.nextState = self.state
        self.lfid = lfid
        self.row = row
        self.col = col

    def is_alive(self):
        """Returns true if the LifeForm is alive, false otherwise."""
        if self.state == self.STATE_ALIVE:
            return True
        return False

    def kill(self, generation):
        """Marks this LifeForm to transition to dead on next commit."""
        self.nextState = self.STATE_DEAD
        if self.state != self.nextState:
            self.transitions.append((generation, self.nextState))

    def birth(self, generation):
        """Marks this LifeForm to transition to alive on next commit."""
        self.nextState = self.STATE_ALIVE
        if self.state != self.nextState:
            self.transitions.append((generation, self.nextState))

    def commit(self):
        """Sets the current state to the state dictated by a previous call to
        kill() or birth()
        """
        self.state = self.nextState

    def get_transition_count(self):
        return len(self.transitions)

    def transitions_to_string(self):
        return ','.join(map(str, self.transitions))

    def __repr__(self):
        return "LifeForm[lfid=%d,row=%d,col=%d]" % (self.lfid, self.row, \
          self.col)
