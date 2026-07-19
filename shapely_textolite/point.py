from shapely.geometry import Point as ShapelyPoint

from logic_textolite import Point as BasePoint


class Point(BasePoint):
    """Реализация точки на базе Shapely."""

    def __init__(
        self,
        x: float | ShapelyPoint = 0.0,
        y: float | None = None,
    ) -> None:
        if isinstance(x, ShapelyPoint):
            self._shapely_point = x

        else:
            if y is None:
                raise ValueError(
                    "Ошибка: при создании точки через числовые координаты "
                    "аргумент 'y' является обязательным и не может быть None."
                )

            self._shapely_point = ShapelyPoint(x, y)

    @property
    def x(self) -> float:
        """Возвращает координату X из объекта Shapely."""
        return float(self._shapely_point.x)

    @property
    def y(self) -> float:
        """Возвращает координату Y из объекта Shapely."""
        return float(self._shapely_point.y)

    @property
    def shapely_geom(self) -> ShapelyPoint:
        """Возвращает низкоуровневый геометрический объект Shapely."""
        return self._shapely_point

    def to_tuple(self) -> tuple[float, float]:
        """Экспортирует координаты в виде кортежа (x, y)."""
        return self.x, self.y
