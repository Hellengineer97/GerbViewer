from shapely.geometry.base import BaseGeometry

from logic_textolite import Trace as BaseTrace

from .shape import Shape


class Trace(BaseTrace):
    """Реализация дорожки на уровне boardview с Shapely-геометрией."""
    def __init__(
        self,
        shape: Shape = Shape(),
        net: str = 'NoNameNet',
    ) -> None:
        super().__init__(shape)
        self.net: str = net

    @property
    def shapely_geom(self) -> BaseGeometry:
        """Возвращает низкоуровневый геометрический объект Shapely."""
        return self.shape.shapely_geom
