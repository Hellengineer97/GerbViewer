from shapely.geometry import GeometryCollection
from shapely.geometry.base import BaseGeometry

from gerbviewlib.logic_textolite.shape import Shape as BaseShape


class Shape(BaseShape):
    """Реализация геометрической формы на базе Shapely."""

    def __init__(self, shapely_geometry: BaseGeometry | None = None) -> None:
        if shapely_geometry is not None:
            if not isinstance(shapely_geometry, BaseGeometry):
                raise TypeError(
                    "Ошибка: геометрия должна быть нативным объектом Shapely "
                    "(например, LineString или Polygon)."
                )
            self._shapely_geometry = shapely_geometry
        else:
            self._shapely_geometry = GeometryCollection()

    @property
    def shapely_geom(self) -> BaseGeometry:
        """Возвращает низкоуровневый геометрический объект Shapely."""
        return self._shapely_geometry

    @property
    def is_empty(self) -> bool:
        """Возвращает True, если геометрический объект не содержит точек."""
        return bool(self._shapely_geometry.is_empty)
