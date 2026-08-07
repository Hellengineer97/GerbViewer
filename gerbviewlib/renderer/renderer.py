from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Tuple

from ..boardview import Textolite, CuLayer, SilkLayer, PadsLayer, Via
from shapely.geometry.base import BaseGeometry
from itertools import chain

env = Environment(
    loader=FileSystemLoader('gerbviewlib/renderer/template'),
    autoescape=select_autoescape(['svg'])
)
template = env.get_template('boardview_template.svg')


class Renderer:
    def get_path_svg_from_Shapely_geom(self,
                                       shapely_geom: BaseGeometry,
                                       net_name: str = 'NoNameNet') -> str:
        """Генерирует path из Shapely геометрии"""
        if shapely_geom.is_empty:
            return ''
        shapely_geom_simplify = shapely_geom.simplify(
            tolerance=0.05,
            preserve_topology=True,
        )
        all_rings = chain((shapely_geom_simplify.exterior,),
                          shapely_geom_simplify.interiors)
        d = ' '.join(
            f"M {coords[0]} L {' '.join(coords[1:])} Z"
            for ring in all_rings
            for coords in [[f"{x:.2f},{y:.2f}" for x, y in ring.coords]]
        )
        return f'<path class="{net_name}" tabindex="0" d="{d}" />'

    def get_g_svg_from_Pads_layer(self,
                                    Pads_layer: PadsLayer,
                                    class_name: str = "PadsLayer") -> str:
            """Генерирует path из слоя падов и пакует в его g тег"""
            paths = []
            for pad in Pads_layer.pads:
                path = self.get_path_svg_from_Shapely_geom(
                    pad.shapely_geom, pad.net)
                paths.append(path)
            return f'<g class="{class_name}">{"".join(paths)}</g>'

    def get_g_svg_from_Silk_layer(self,
                                  Silk_layer: SilkLayer,
                                  class_name: str = "SilkLayer") -> str:
        """Генерирует path из шелкографического слоя и пакует в его g тег"""
        paths = []
        for shape in Silk_layer.shapes:
            path = self.get_path_svg_from_Shapely_geom(
                shape.shapely_geom)
            paths.append(path)
        return f'<g class="{class_name}">{"".join(paths)}</g>'

    def get_g_svg_from_Cu_layer(self,
                                Cu_layer: CuLayer,
                                class_name: str = "CuLayer") -> str:
        """Генерирует path из медного слоя и пакует в его g тег"""
        paths = []
        for trace in Cu_layer.traces:
            path = self.get_path_svg_from_Shapely_geom(
                trace.shapely_geom, trace.net)
            paths.append(path)
        return f'<g class="{class_name}">{"".join(paths)}</g>'

    def calculate_bounds(self,
                         textolite: Textolite
                         ) -> Tuple[float, float, float, float]:
        """
        Вычисляет min_x, min_y, width, height по геометрии shapely в textolite.
        """
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')
        all_shapely_geoms = []
        for layer in textolite.all_layers:
            if isinstance(layer, CuLayer):
                for trace in layer.traces:
                    all_shapely_geoms.append(trace.shapely_geom)
        for shapely_geom in all_shapely_geoms:
            b = shapely_geom.bounds
            min_x = min(min_x, b[0])
            min_y = min(min_y, b[1])
            max_x = max(max_x, b[2])
            max_y = max(max_y, b[3])
        return min_x, min_y, max_x - min_x, max_y - min_y

    def renderSVG(self, textolite: Textolite) -> str:
        min_x, min_y, width, height = self.calculate_bounds(textolite)
        content = ''
        for layer in textolite.all_layers:
            if isinstance(layer, CuLayer):
                content += self.get_g_svg_from_Cu_layer(layer)
            elif isinstance(layer, SilkLayer):
                content += self.get_g_svg_from_Silk_layer(layer)
            elif isinstance(layer, PadsLayer):
                content += self.get_g_svg_from_Pads_layer(layer)
        return template.render(
            min_x=f"{min_x:.1f}",
            min_y=f"{min_y:.1f}",
            width=f"{width:.1f}",
            height=f"{height:.1f}",
            content=content,
        )
