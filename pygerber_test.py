from pygerber.gerber.api import GerberFile
from constant import BOTTOM_GBR_PATH, BOTTOM_SVG_PATH
# 1. Загружаем Gerber-файл платы
gerber = GerberFile.from_file(BOTTOM_GBR_PATH)

# 2. Рендерим файл в геометрию (получаем объект ShapelyImage)
shapely_image = gerber.render_with_shapely()

# 3. Напрямую сохраняем результат в SVG-файл
shapely_image.save_svg(BOTTOM_SVG_PATH)

print(f"Векторный файл успешно сохранен в: {BOTTOM_SVG_PATH}")