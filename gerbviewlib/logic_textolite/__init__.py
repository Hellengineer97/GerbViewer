"""Модуль физической логики и структурной топологии печатной платы.

Не содержит геометрических алгоритмов, выполняя роль высокоуровневого
структурного контейнера для данных топологии.
"""
from .layer import TextoliteSide, CuLayer, PadsLayer, SilkLayer
from .pad import Pad
from .point import Point
from .shape import Shape
from .textolite import Textolite
from .trace import Trace
from .via import Via

__all__ = [
    "Textolite",
    "TextoliteSide",
    "CuLayer",
    "PadsLayer",
    "SilkLayer",
    "Pad",
    "Point",
    "Shape",
    "Trace",
    "Via",
]
