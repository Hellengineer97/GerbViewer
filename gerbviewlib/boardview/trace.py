from logic_textolite import Trace as BaseTrace

from .shape import Shape


class Trace(BaseTrace):
    """Реализация дорожки на уровне boardview с Shapely-геометрией."""

    def __init__(
        self,
        shape: Shape | None = None,
        net: str | None = None,
    ) -> None:
        normalized_shape = shape if shape is not None else Shape()
        super().__init__(normalized_shape)
        self.net: str | None = net
