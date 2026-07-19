from .point import Point


class Via:
    """Базовый класс отверстия в текстолите."""

    def __init__(self, point: Point | None = None):
        self.point = point if point is not None else Point()
