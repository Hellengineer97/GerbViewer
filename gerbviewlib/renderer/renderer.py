from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Tuple

from ..boardview import Textolite


env = Environment(
    loader=FileSystemLoader('gerbviewlib/renderer/template'),
    autoescape=select_autoescape(['svg'])
)
template = env.get_template('boardview_template.svg')


class Renderer:
    def _calculate_bounds(self, textolite: Textolite) -> Tuple[float, float, float, float]:
        """Вычисляет min_x, min_y, width, height по геометриям `textolite`.

        Поведение близко к `BoardView.calculate_bounds`: итерируем все CU-слои,
        пропускаем пустые геометрии и вычисляем общие габариты.
        """
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')

        # собираем все CU-слои: inner + видимые стороны если есть
        layers = []
        if getattr(textolite, 'inner_cu_layers', None):
            layers.extend(textolite.inner_cu_layers)
        top = getattr(textolite, 'top_layer', None)
        if top is not None and getattr(top, 'cu', None) is not None:
            layers.append(top.cu)
        bottom = getattr(textolite, 'bottom_layer', None)
        if bottom is not None and getattr(bottom, 'cu', None) is not None:
            layers.append(bottom.cu)

        for layer in layers:
            for trace in getattr(layer, 'traces', []):
                geom = getattr(getattr(trace, 'shape', None), 'shapely_geom', None)
                b = geom.bounds
                min_x = min(min_x, b[0])
                min_y = min(min_y, b[1])
                max_x = max(max_x, b[2])
                max_y = max(max_y, b[3])

        if min_x == float('inf'):
            # fallback пустой страницы
            min_x = 0.0
            min_y = 0.0
            max_x = 1.0
            max_y = 1.0

        width = max_x - min_x
        height = max_y - min_y
        return min_x, min_y, width, height

    def renderSVG(self, textolite: Textolite) -> str:
        """Рендер `Textolite` в SVG, используя Jinja2-шаблон.

        Шаблон ожидает переменные `min_x`, `min_y`, `width`, `height` и
        `content` (HTML/SVG внутри `<g>`). Здесь `content` пока оставляем
        простым: пустой контейнер — пользователь может заполнить позже.
        """
        min_x, min_y, width, height = self._calculate_bounds(textolite)
        rendered = template.render(
            min_x=f"{min_x:.1f}",
            min_y=f"{min_y:.1f}",
            width=f"{width:.1f}",
            height=f"{height:.1f}",
            content="<!-- layers will be rendered here -->",
        )
        return rendered