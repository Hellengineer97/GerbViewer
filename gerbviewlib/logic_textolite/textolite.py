from .layer import TextoliteSide, InnerCuLayers, ViasLayer


class Textolite:
    """Базовый класс текстолита платы."""

    def __init__(
        self,
        inner_cu_layers: InnerCuLayers | None = None,
        top_layer: TextoliteSide | None = None,
        bottom_layer: TextoliteSide | None = None,
        vias: ViasLayer | None = None,
    ):
        self.inner_cu_layers = (
            inner_cu_layers if inner_cu_layers is not None else InnerCuLayers()
        )
        self.top_layer = (
            top_layer if top_layer is not None else TextoliteSide()
        )
        self.bottom_layer = (
            bottom_layer if bottom_layer is not None else TextoliteSide()
        )
        self.vias = vias if vias is not None else ViasLayer()
