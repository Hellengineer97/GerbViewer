from shapely.geometry.base import BaseGeometry

from gerbviewlib.logic_textolite import Pad as BasePad


class Pad(BasePad):
    """Контакт на уровне boardview с сетевой и компонентной информацией."""

    def __init__(
        self,
        shape=None,
        net: str | None = None,
        component: str | None = None,
        name: str | None = None,
    ) -> None:
        super().__init__(shape)
        self.net: str | None = net
        self.component: str | None = component
        self.name: str | None = name

    @property
    def shapely_geom(self) -> BaseGeometry:
        """Возвращает низкоуровневый геометрический объект Shapely."""
        return self.shape.shapely_geom
