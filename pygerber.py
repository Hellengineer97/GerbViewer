from pygerber.gerberx3.api import Layer, LayerParams
from shapely.geometry import base
from shapely.ops import unary_union

def get_shapely_from_gerber(file_path: str):
    """
    Читает Gerber-файл и возвращает объединенную геометрию Shapely.
    """
    # 1. Создаем объект слоя. 
    # PyGerber сам определит тип (медь, маска и т.д.)
    layer = Layer(
        params=LayerParams(
            source_path=file_path,
        )
    )

    # 2. Генерируем набор геометрии (Shapely-объекты)
    # Этот метод создаст список полигонов, учитывая толщину линий и форму апертур
    shapes = layer.as_shapely_objects()

    # 3. Выполняем "Unite" (слияние всех накладывающихся элементов)
    unified = unary_union(shapes)

    return unified

# Пример использования:
if __name__ == "__main__":
    path_to_gerber = "your_file.gbr"  # укажите путь к вашему файлу
    merged_geometry = get_shapely_from_gerber(path_to_gerber)

    if merged_geometry.is_empty:
        print("Фигуры не найдены или файл пуст.")
    else:
        print(f"Тип полученной геометрии: {merged_geometry.geom_type}")
        # Теперь с merged_geometry можно работать как с обычным объектом Shapely
        # Например, найти площадь:
        print(f"Площадь объединенной фигуры: {merged_geometry.area}")