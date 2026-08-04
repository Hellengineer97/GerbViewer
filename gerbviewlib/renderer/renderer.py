from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Tuple
from xml.sax.saxutils import escape

from ..boardview import Textolite


env = Environment(
    loader=FileSystemLoader('gerbviewlib/renderer/template'),
    autoescape=select_autoescape(['svg'])
)
template = env.get_template('boardview_template.svg')


class Renderer:
    def _calculate_bounds(self, textolite: Textolite) -> Tuple[float, float, float, float]:
        """
        Вычисляет min_x, min_y, width, height по геометриям `textolite`.
        """
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')
        layers = list(textolite.inner_cu_layers)
        layers.append(textolite.top_layer.cu)
        layers.append(textolite.bottom_layer.cu)

        for layer in layers:
            for trace in layer.traces:
                geom = trace.shape.shapely_geom
                b = geom.bounds
                min_x = min(min_x, b[0])
                min_y = min(min_y, b[1])
                max_x = max(max_x, b[2])
                max_y = max(max_y, b[3])

        width = max_x - min_x
        height = max_y - min_y
        return min_x, min_y, width, height

    def _path_d(self, geom, min_x: float, min_y: float) -> str:
        geom_type = geom.geom_type
        if geom_type in ('LineString', 'LinearRing'):
            coords = list(geom.coords)
            d = f'M {coords[0][0] - min_x} {coords[0][1] - min_y}'
            for x, y in coords[1:]:
                d += f' L {x - min_x} {y - min_y}'
            return d

        if geom_type == 'Polygon':
            exterior = list(geom.exterior.coords)
            d = self._path_d(type('G', (), {'geom_type': 'LineString', 'coords': exterior}), min_x, min_y)
            for interior in geom.interiors:
                interior_coords = list(interior.coords)
                d += ' ' + self._path_d(type('G', (), {'geom_type': 'LineString', 'coords': interior_coords}), min_x, min_y)
            return d

        if geom_type.startswith('Multi'):
            return ' '.join(self._path_d(part, min_x, min_y) for part in geom.geoms)

        return ''

    def _render_layer(self, layer, min_x: float, min_y: float) -> str:
        paths = []
        for trace in layer.traces:
            d = self._path_d(trace.shape.shapely_geom, min_x, min_y)
            net_name = trace.net.name if trace.net is not None else 'none'
            paths.append(
                f'<path d="{escape(d)}" class="{escape(net_name)}" fill="none" stroke="#000" stroke-width="1" />'
            )
        layer_class = escape(layer.__class__.__name__)
        return f'<g class="{layer_class}">{"".join(paths)}</g>'

    def renderSVG(self, textolite: Textolite) -> str:
        min_x, min_y, width, height = self._calculate_bounds(textolite)
        layers = list(textolite.inner_cu_layers)
        layers.append(textolite.top_layer.cu)
        layers.append(textolite.bottom_layer.cu)
        content = ''.join(self._render_layer(layer, min_x, min_y) for layer in layers)
        rendered = template.render(
            min_x=f"{min_x:.1f}",
            min_y=f"{min_y:.1f}",
            width=f"{width:.1f}",
            height=f"{height:.1f}",
            content=content,
        )
        return rendered
