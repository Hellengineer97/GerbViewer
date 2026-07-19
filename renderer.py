import logging
from pathlib import Path
from logic_textolite import Board
from constants import JINJA_ENV

logger = logging.getLogger(__name__)


class Renderer:
    @property
    def board(self) -> Board:
        return self._board

    @board.setter
    def board(self, board: Board):
        self._board = board if board is not None else Board()

    def __init__(self, board: Board | None = None):
        self.board = board

    def render(self, export_svg_path: Path):
        JINJA_ENV.get_template("boardview.svg").stream(
            board=self.board
        ).dump(str(export_svg_path), encoding="utf-8")

        logger.info(f"SVG успешно сохранён: {export_svg_path.absolute()}")
