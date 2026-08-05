from __future__ import annotations

from typing import List, Optional

from .layer import CuLayer, Layer, TextoliteSide
from .via import Via
from ..logic_textolite.textolite import Textolite as BaseTextolite


class Textolite(BaseTextolite):
    """
    В текущей реализации наследует поведение базового класса,
    и возвращает список слоёв в порядке от верхнего к нижнему (all_layers).
    """

    def __init__(
        self,
        inner_cu_layers: Optional[List[CuLayer]] = None,
        top_layer: Optional[TextoliteSide] = None,
        bottom_layer: Optional[TextoliteSide] = None,
        vias: Optional[List[Via]] = None,
    ):
        super().__init__(
            inner_cu_layers=inner_cu_layers,
            top_layer=top_layer,
            bottom_layer=bottom_layer,
            vias=vias,
        )

    @property
    def all_layers(self) -> List[Layer]:
        layers = []
        if self.vias:
            layers.append(self.vias)
        if self.top_layer:
            layers.append(self.top_layer.silk)
            layers.append(self.top_layer.pads)
            layers.append(self.top_layer.cu)
        if self.inner_cu_layers:
            layers.extend(self.inner_cu_layers)
        if self.bottom_layer:
            layers.append(self.bottom_layer.cu)
            layers.append(self.bottom_layer.pads)
            layers.append(self.bottom_layer.silk)
        return layers
