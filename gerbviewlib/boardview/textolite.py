from __future__ import annotations

from typing import List, Optional

from .layer import CuLayer, TextoliteSide
from .via import Via
from ..logic_textolite.textolite import Textolite as BaseTextolite


class Textolite(BaseTextolite):
    """
    В текущей реализации просто наследует поведение базового
    `logic_textolite.Textolite`, но принимает и возвращает
    объекты уровня `boardview`.
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
