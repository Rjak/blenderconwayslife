from golmodel.universe import Universe

class Simulation(object):
    """Computes the lives and deaths of lifeforms at each generation"""

    def __init__(self, universe):
        self.universe = universe
        self.generation = 0
        self.births = 0
        self.deaths = 0

    def advance(self):
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
        self.commit()

    def commit(self):
        for x in range (0, self.universe.rows):
            for y in range (0, self.universe.cols):
                lf = self.universe.get_life_form(x, y)
                lf.commit()
