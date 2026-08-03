from net_generator import NetGenerator
from renderer import Renderer
from .boardview import Textolite


class BoardView:
    def __init__(
        self,
        textolite: Textolite,
        renderer: Renderer,
        net_generator: NetGenerator,
    ):
        self.textolite = textolite
        self.renderer = renderer
        self.net_generator = net_generator

    def build_nets(self) -> None:
        self.net_generator.generate(self.textolite)

    def render_svg(self) -> str:
        return self.renderer.render(self.textolite)
