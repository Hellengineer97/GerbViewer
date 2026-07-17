import logging
from pathlib import Path
from board import Board
from constants import JINJA_ENV

logger = logging.getLogger(__name__)


class Renderer:
    def __init__(self, board: Board | None = None):
        self.board = board

    def render(self, export_svg_path: Path):
        JINJA_ENV.get_template("none.svg").stream(
            viewbox=self.board.bounds.viewbox,
            board=self.board
        ).dump(str(export_svg_path), encoding="utf-8")

        logger.info(f"SVG успешно сохранён: {export_svg_path.absolute()}")
