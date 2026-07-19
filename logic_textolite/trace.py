from .shape import Shape


class Trace:
    """Базовый класс дорожки."""

    def __init__(self, shape: Shape | None = None):
        self.shape = shape if shape is not None else Shape()
