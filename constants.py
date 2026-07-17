from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Базовая папка вашего проекта
BASE_DIR = Path(__file__).parent

# Пути к ресурсам
TEMPLATES_DIR = BASE_DIR / "templates"

# Общие глобальные настройки (настраиваются ОДИН раз при запуске)
JINJA_ENV = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


BOTTOM_GBR_PATH = 'gbr_source/Bottom.gbr'
BOTTOM_SVG_PATH = 'svg_export/bottom.svg'
TOP_GBR_PATH = 'gbr_source/Top.gbr'
TOP_SVG_PATH = 'svg_export/Top.svg'
OUTPUT_SVG_PATH = 'svg_export/output.svg'
DRILL_GBR_PATH = 'gbr_source/drill.gbr'
TRACES_SVG_PATH = 'svg_export/traces_svg_path.svg'
CU5_GBR_PATH = 'gbr_source/Cu5.gbr'
BOARDVIEW_SVG_PATH = 'svg_export/BoardView.svg'
