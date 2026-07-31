from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from shapely.geometry.base import BaseGeometry

from logic_textolite import (
    Layer as BaseLayer,
    CuLayer as BaseCuLayer,
    SilkLayer as BaseSilkLayer,
    PadsLayer as BasePadsLayer,
    TextoliteSide as BaseTextoliteSide,
)

from .pad import Pad
from .shape import Shape
from .trace import Trace

from pygerber.gerber.api import GerberFile

GerberSource = str | Path | GerberFile


def _load_gerber_source(source: str | Path | Any) -> Any:
    if isinstance(source, (str, Path)):
        return GerberFile.from_file(str(source))

    if isinstance(source, GerberFile):
        return source

    raise TypeError(
        'gerber_source должен быть путем к файлу или экземпляром '
        'pygerber.GerberFile'
    )


class Layer(BaseLayer):
    """Обёртка слоя boardview с поддержкой Gerber-источника."""

    def __init__(self, gerber_source: GerberSource):
        self._pygerber_object: GerberFile = _load_gerber_source(gerber_source)

        if isinstance(gerber_source, (str, Path)):
            self._gerber_source = Path(gerber_source)

        self._parse_gerber()

    def _unary_shapely_geometry(self) -> Optional[BaseGeometry]:
        return self.pygerber_object.render_with_shapely()._result.shape

    def _split_geometries(
        self,
        geometry: Optional[BaseGeometry],
    ) -> list[BaseGeometry]:
        if hasattr(geometry, 'geoms'):
            return list(geometry.geoms)
        return [geometry]

    def _parse_gerber(self) -> None:
        """Внутренний метод разбора Gerber, вызываемый при инициализации."""
        raise NotImplementedError


class CuLayer(BaseCuLayer, Layer):
    """Обёртка медного медного слоя boardview."""

    def __init__(
        self,
        gerber_source: str | Path | Any | None = None,
        traces=None,
    ):
        BaseCuLayer.__init__(self, traces=traces)
        Layer.__init__(self, gerber_source=gerber_source)

    def _parse_gerber(self) -> None:
        self.traces = [
            Trace(Shape(shape))
            for shape in self._split_geometries(self._unary_shapely_geometry())
        ]


class SilkLayer(BaseSilkLayer, Layer):
    """Обёртка шелкографического слоя boardview."""

    def __init__(
        self,
        gerber_source: str | Path | Any | None = None,
        shapes=None,
    ):
        BaseSilkLayer.__init__(self, shapes=shapes)
        Layer.__init__(self, gerber_source=gerber_source)

    def _parse_gerber(self) -> None:
        self.shapes = [
            Shape(shape)
            for shape in self._split_geometries(self._unary_shapely_geometry())
        ]


class PadsLayer(BasePadsLayer, Layer):
    """Обёртка слоя контактных площадок boardview."""

    def __init__(
        self,
        gerber_source: str | Path | Any | None = None,
        pads=None,
    ):
        BasePadsLayer.__init__(self, pads=pads)
        Layer.__init__(self, gerber_source=gerber_source)

    def _parse_gerber(self) -> None:
        self.pads = [
            Pad(shape=Shape(shape))
            for shape in self._split_geometries(self._unary_shapely_geometry())
        ]


class TextoliteSide(BaseTextoliteSide):
    """Обёртка видимой стороны текстолита на уровне boardview."""
    pass
