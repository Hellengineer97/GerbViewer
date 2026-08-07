from shapely.geometry import Point as ShapelyPoint

from gerbviewlib.logic_textolite import Via as BaseVia
from .point import Point


class Via(BaseVia):
    """Via на boardview точкой на базе Shapely."""

    def __init__(
        self,
        point: Point | ShapelyPoint | tuple[float, float] | None = None,
        net: str | None = None,
    ) -> None:
        normalized_point = self._normalize_point(point)
        super().__init__(normalized_point)
        self.net: str | None = net

    @staticmethod
    def _normalize_point(
        point: Point | ShapelyPoint | tuple[float, float] | None,
    ) -> Point:
        if point is None:
            return Point(0.0, 0.0)

        if isinstance(point, Point):
            return point

        if isinstance(point, ShapelyPoint):
            return Point(point)

        if isinstance(point, tuple) and len(point) == 2:
            return Point(point[0], point[1])

        raise TypeError(
            'Via принимает boardview.Point, Shapely Point или tuple[x, y]'
        )
