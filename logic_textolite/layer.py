from .pad import Pad
from .trace import Trace
from .shape import Shape


class Layer:
    """Базовый класс слоя"""


class CuLayer(Layer):
    """Слой меди"""
    def __init__(self, traces: list[Trace] | None = None):
        self.traces = traces if traces is not None else []


class SilkLayer(Layer):
    """Слой шелкографии"""
    def __init__(self, shapes: list[Shape] | None = None):
        self.shapes = shapes if shapes is not None else []


class PadsLayer(Layer):
    """Слой контактов"""
    def __init__(self, pads: list[Pad] | None = None):
        self.pads = pads if pads is not None else []


class TextoliteSide:
    """Логическая видимая сторона текстолита"""
    def __init__(self,
                 cu_layer: CuLayer | None = None,
                 silk_layer: SilkLayer | None = None,
                 pads_layer: PadsLayer | None = None):
        self.cu = cu_layer if cu_layer is not None else CuLayer()
        self.silk = silk_layer if silk_layer is not None else SilkLayer()
        self.pads = pads_layer if pads_layer is not None else PadsLayer()
