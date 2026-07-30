from .layer import CuLayer, TextoliteSide
from .via import Via


class Textolite:
    """Базовый класс текстолита платы."""

    def __init__(
        self,
        inner_cu_layers: list[CuLayer] | None = None,
        top_layer: TextoliteSide | None = None,
        bottom_layer: TextoliteSide | None = None,
        vias: list[Via] | None = None,
    ):
        self.inner_cu_layers = (
            inner_cu_layers if inner_cu_layers is not None else []
        )
        self.top_layer = (
            top_layer if top_layer is not None else TextoliteSide()
        )
        self.bottom_layer = (
            bottom_layer if bottom_layer is not None else TextoliteSide()
        )
        self.vias = vias if vias is not None else []
