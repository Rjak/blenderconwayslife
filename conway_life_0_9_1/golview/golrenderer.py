import abc

class GOLRenderer(object):
    """Game of Life Renderer Base Class"""

    @abc.abstractmethod
    def render(self, universe):
        """Called by the driver to render one generation of the sim"""
        return
    
    def get_frame_delay(self):
        return 0
