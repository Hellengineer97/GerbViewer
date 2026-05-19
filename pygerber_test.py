from pygerber.gerber.api import GerberFile
from constant import BOTTOM_GBR_PATH, BOTTOM_SVG_PATH, TOP_GBR_PATH, DRILLS_GBR_PATH
# 1. Загружаем Gerber-файл платы
gerber_bot = GerberFile.from_file(BOTTOM_GBR_PATH)
gerber_top = GerberFile.from_file(TOP_GBR_PATH)
gerber_drills = GerberFile.from_file(DRILLS_GBR_PATH)
# 2. Рендерим файл в геометрию (получаем объект ShapelyImage)
shapely_image_bot = gerber_bot.render_with_shapely()
shapely_image_top = gerber_top.render_with_shapely()
shapely_image_drills = gerber_drills.render_with_shapely()
# 3. Напрямую сохраняем результат в SVG-файл
# shapely_image.save_svg(BOTTOM_SVG_PATH)

# print(f"Векторный файл успешно сохранен в: {BOTTOM_SVG_PATH}")
from shapely.geometry import MultiPolygon, GeometryCollection

main_shape = shapely_image_drills._result.shape

centers = []

for geom in main_shape.geoms:
  # Для каждого отдельного отверстия берем центр
    c = geom.centroid
    centers.append((c.x, c.y))

print(f"Извлечено центров: {len(centers)}")
for i, (x, y) in enumerate(centers):
    print(f"Центр {i+1}: X={x:.4f}, Y={y:.4f}")