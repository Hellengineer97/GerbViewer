import svgelements
from constant import BOTTOM_SVG_PATH

# 1. Парсим файл. На выходе получаем объект класса SVG (который является наследником Group)
svg = svgelements.SVG.parse(BOTTOM_SVG_PATH)

# 2. Так как svgelements отдал размеры как float, берем их напрямую
current_width = svg.width
current_height = svg.height

SCALE = 10.0  # Коэффициент увеличения

# 3. Меняем внешние атрибуты тега <svg> для монитора
svg.width = current_width * SCALE
svg.height = current_height * SCALE

svg.transform.scale(SCALE)

# 4. Перезаписываем файл
with open(BOTTOM_SVG_PATH, "w", encoding="utf-8") as f:
    f.write(svg.string_xml())

print("Размер холста успешно увеличен в 10 раз!")