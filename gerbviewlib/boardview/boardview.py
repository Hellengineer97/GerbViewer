from gerbviewlib.net_generator import NetGenerator
from gerbviewlib.renderer import Renderer
from .textolite import Textolite


class BoardView:
    """
    когда создается объект класса создает пустой текстолит.
    пустой рендерер а также пустой генератор сетей
    а когда сздает пустой текстолит то он создает пустые слои
    и пустые списки слоев.
    """
    def __init__(
        self,
        renderer: Renderer | None = None,
        net_generator: NetGenerator | None = None,
        textolite: Textolite | None = None,
    ):
        self.textolite = (
            textolite if textolite is not None else Textolite()
        )
        self.renderer = (
            renderer if renderer is not None else Renderer()
        )
        self.net_generator = (
            net_generator if net_generator is not None else NetGenerator()
        )

    def build_nets(self) -> None:
        """Генерирует сети для textolite с помощью net_generator."""
        if self.net_generator is None:
            raise ValueError("net_generator не установлен.")
        self.net_generator.generate(self.textolite)

    def render_svg(self) -> str:
        """Рендерит textolite в SVG с помощью renderer."""
        if self.renderer is None:
            raise ValueError("renderer не установлен.")
        return self.renderer.renderSVG(self.textolite)
