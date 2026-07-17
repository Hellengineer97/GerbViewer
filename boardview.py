from net_generator import NetGenerator
from renderer import Renderer
from board import Board


class Boadview:
    def _renderer_init(self):
        self._renderer.board = self.board

    def _net_generator_init(self):
        self._net_generator.board = self.board

    @property
    def renderer(self) -> Renderer:
        return self._renderer

    @renderer.setter
    def renderer(self, new_renderer: Renderer):
        self._renderer = new_renderer
        self._renderer_init()

    @property
    def net_generator(self) -> NetGenerator:
        return self._net_generator

    @net_generator.setter
    def net_generator(self, new_net_generator: NetGenerator):
        self._net_generator = new_net_generator
        self._net_generator_init()

    def __init__(self,
                 board: Board,
                 renderer: Renderer = None,
                 net_generator: NetGenerator = None):
        self.board = board
        self._renderer = renderer or Renderer(board)
        self._net_generator = net_generator or NetGenerator(board)
