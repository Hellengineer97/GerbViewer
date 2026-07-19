from .shape import Shape


class Pad:
    """Базовый класс контакта, не покрытого изоляцией."""

    def __init__(self, shape: Shape | None = None):
        self.shape = shape if shape is not None else Shape()
