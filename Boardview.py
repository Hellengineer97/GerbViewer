from pygerber.gerber.api import GerberFile
from pygerber.vm.shapely import ShapelyVirtualMachine
from shapely.geometry import Point
from shapely.strtree import STRtree
from collections import deque


class GetDrillVirtualMachine(ShapelyVirtualMachine):
    """
    Переделанная вирт машина, чтобы вытягивать координаты отверстий.
    Обрабатывает только команду D03
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Список будет жить внутри конкретного экземпляра машины
        self.drill_points = []

    def on_paste_layer_eager(self, command):
        # Ловим D03, забираем чистый вектор центра
        self.drill_points.append((command.center.x, command.center.y))


class CustomPolygon:
    """
    Переделанный класс полигона который генерит SVG элемент без лишнего мусора
    """

    def __init__(self, poly_object):
        self._poly = poly_object

    def __getattr__(self, name):
        return getattr(self._poly, name)

    def svg(self, net_name: str):
        if self.is_empty:
            return "<g />"

        exterior_coords = ["{},{}".format(*c) for c in self.exterior.coords]
        interior_coords = [
            ["{},{}".format(*c) for c in
             interior.coords] for interior in self.interiors
        ]

        all_rings = [exterior_coords] + interior_coords
        path_segments = []
        for coords in all_rings:
            if len(coords) > 0:
                path_segments.append(
                    f"M {coords[0]} L {' '.join(coords[1:])} Z")

        path = " ".join(path_segments)
        return f'<path class="{net_name}" tabindex="0" d="{path}" />'


class Trace:
    """Класс одной дорожки"""
    def __init__(self, shapely_polygon: CustomPolygon, layer = None):
        self.net = None
        self.shapely_polygon = shapely_polygon
        self.layer = layer

    def get_svg_path(self):
        return self.shapely_polygon.svg(self.net.name if self.net else "NoNameNet")


class Drill:
    """Класс одного отверстия на плате, соединяющего дорожки"""
    def __init__(self, point: Point = None, x: float = None, y: float = None):
        if point is not None:
            self.point = point
        elif x is not None and y is not None:
            self.point = Point(x, y)
        else:
            raise ValueError(
                "Необходимо передать либо объект point, либо координаты x и y")

        self.net = None
        self.connections = {}

    @property
    def x(self) -> float:
        return self.point.x

    @property
    def y(self) -> float:
        return self.point.y


class Net:
    """Тут описаны связи между дорожками и отверстиями"""
    def __init__(self, name: str):
        self.name = name
        self.traces = set()
        self.drills = set()

    def add_trace(self, trace: Trace):
        trace.net = self
        self.traces.add(trace)

    def add_drill(self, drill: Drill):
        drill.net = self
        self.drills.add(drill)

    def __repr__(self):
        """Красивое отображение цепи при выводе через print"""
        return f"Net({self.name}, Polygons: {
            len(self.traces)}, Drills: {len(self.drills)})"


class Layer:
    def __init__(self, gerberfile: GerberFile, name: str = "Layer"):
        self.gerberfile = gerberfile
        self.name = name
        self.traces = self.get_traces(self.gerberfile)

    def get_traces(self, gerberfile: GerberFile):
        rvmc = gerberfile._get_rvmc()
        shvm = ShapelyVirtualMachine()
        shapely_result = shvm.run(rvmc)
        custom_polygons = [CustomPolygon(geom) for geom in
                           shapely_result.shape.geoms]
        traces = []
        for poly in custom_polygons:
            trace = Trace(poly)
            trace.layer = self
            traces.append(trace)
        return traces

class BoardBounds:
    def __init__(self,
                 min_x = float('inf'),
                 min_y = float('inf'),
                 max_x = float('-inf'),
                 max_y = float('-inf')
                 ):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.width = max_x - min_x
        self.height = max_y - min_y

class BoardView:
    def __init__(self,
                 gerber_files: list[GerberFile], drills_file: GerberFile):
        self.gerber_files = gerber_files
        self.drills_file = drills_file
        self.drills = self.get_drill(drills_file)
        self.layers = self.get_layers(gerber_files)
        self.nets: dict[str, Net] = {}
        self.net_counter = 1
        self.build_nets()
        self.bounds: BoardBounds = self.calculate_bounds()

    def get_drill(self, gerberfile: GerberFile) -> list:
        rvmc = gerberfile._get_rvmc()
        get_drill_vm = GetDrillVirtualMachine()
        get_drill_vm.run(rvmc)
        drills = []
        for point in get_drill_vm.drill_points:
            drills.append(Drill(x=point[0], y=point[1]))
        return drills

    def get_layers(self, gerber_files: list[GerberFile]):
        return [Layer(gf, name=f"layer_{i}") for i, gf in enumerate(gerber_files)]
    
    def build_nets(self):
        """Основной метод построения сетей"""
        print("=== Запуск построения электрических сетей ===")

        all_objects = list(self.drills)
        for layer in self.layers:
            all_objects.extend(layer.traces)

        if not all_objects:
            print("Нет объектов для обработки")
            return

        # Создаём spatial index
        geoms = []
        for obj in all_objects:
            if isinstance(obj, Trace):
                geoms.append(obj.shapely_polygon._poly)
            else:
                geoms.append(obj.point)   # без буфера

        tree = STRtree(geoms)
        visited = set()

        for obj in all_objects:
            if obj in visited:
                continue

            net_name = f"net{self.net_counter}"
            self.net_counter += 1
            current_net = Net(name=net_name)

            self._flood_fill(obj, current_net, tree, visited, all_objects)

            self.nets[net_name] = current_net

        print(f"Готово! Создано сетей: {len(self.nets)}")

    def _flood_fill(self, start_obj, current_net: Net, tree, visited, all_objects):
        queue = deque([start_obj])
        visited.add(start_obj)

        while queue:
            current = queue.popleft()

            if isinstance(current, Trace):
                current_net.add_trace(current)
            else:
                current_net.add_drill(current)

            neighbors = self._find_neighbors(current, tree, all_objects)
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    def _find_neighbors(self, obj, tree, all_objects):
        """Исправленная версия"""
        neighbors = []

        if isinstance(obj, Trace):
            geom = obj.shapely_polygon._poly
            layer_name = obj.layer.name if obj.layer else None

            candidates_idx = tree.query(geom, predicate='intersects')

            for idx in candidates_idx:
                candidate = all_objects[idx]
                if candidate is obj:
                    continue

                if isinstance(candidate, Trace):
                    # Только на одном слое
                    if layer_name and candidate.layer and candidate.layer.name == layer_name:
                        if geom.intersects(candidate.shapely_polygon._poly):
                            neighbors.append(candidate)

                elif isinstance(candidate, Drill):
                    # Trace всегда может подключаться к Drill
                    neighbors.append(candidate)

        else:  # Drill
            point = obj.point
            # Используем buffer для надёжности (маленький!)
            candidates_idx = tree.query(point.buffer(0.05), predicate='intersects')

            for idx in candidates_idx:
                candidate = all_objects[idx]
                if isinstance(candidate, Trace):
                    neighbors.append(candidate)

        return neighbors
    
    def calculate_bounds(self):
        """Вычисляет габариты всей платы"""
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')

        for layer in self.layers:
            for trace in layer.traces:
                poly = trace.shapely_polygon._poly
                if poly.is_empty or poly.bounds is None:
                    continue
                
                bounds = poly.bounds  # (minx, miny, maxx, maxy)
                min_x = min(min_x, bounds[0])
                min_y = min(min_y, bounds[1])
                max_x = max(max_x, bounds[2])
                max_y = max(max_y, bounds[3])

        return BoardBounds(min_x, min_y, max_x, max_y)
