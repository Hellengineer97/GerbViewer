from asyncio.log import logger
import math

from net_generator import NetGenerator
from renderer import Renderer
from logic_textolite import Board


class Bounds:
    """
    Границы платы.
    По дефолу зодаются с бесконечностями, которые надо потом просчитать.
    """
    def __init__(self,
                 min_x: float = float('inf'),
                 min_y: float = float('inf'),
                 max_x: float = float('-inf'),
                 max_y: float = float('-inf')
                 ):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    @property
    def width(self) -> float:
        return self.max_x - self.min_x

    @property
    def height(self) -> float:
        return self.max_y - self.min_y

    @property
    def viewbox(self) -> tuple[float, float, float, float] | None:
        if not all(math.isfinite(c) for c in (self.min_x, self.min_y,
                                              self.max_x, self.max_y)):
            logger.warning(
                f"Запрошен viewBox для пустых или некорректных границ. "
                f"Текущие значения: min_x={self.min_x}, min_y={self.min_y}, "
                f"max_x={self.max_x}, max_y={self.max_y}. "
                f"Возвращено значение None."
            )
            return None
        return (self.min_x, self.min_y, self.width, self.height)


class Boadview:
    @property
    def renderer(self) -> Renderer:
        return self._renderer

    @renderer.setter
    def renderer(self, new_renderer: Renderer):
        self._renderer = new_renderer
        self._renderer.board = self.board

    @property
    def net_generator(self) -> NetGenerator:
        return self._net_generator

    @net_generator.setter
    def net_generator(self, new_net_generator: NetGenerator):
        self._net_generator = new_net_generator
        self._net_generator.board = self.board

    def __init__(self,
                 board: Board,
                 renderer: Renderer = None,
                 net_generator: NetGenerator = None):
        self.board = board
        self._renderer = renderer or Renderer(board)
        self._net_generator = net_generator or NetGenerator(board)

