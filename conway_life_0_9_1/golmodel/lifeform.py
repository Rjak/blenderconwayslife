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
