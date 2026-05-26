from pygerber.gerber.api import GerberFile
from pygerber.vm.shapely import ShapelyVirtualMachine
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
from constant import (BOTTOM_GBR_PATH, TOP_GBR_PATH, DRILL_GBR_PATH,
                      TOP_SVG_PATH, BOTTOM_SVG_PATH)


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
    """Класс одной медной дорожки"""
    def __init__(self, shapely_polygon: CustomPolygon, net=None):
        self._net = net
        self.shapely_polygon = shapely_polygon

    @property
    def net(self):
        return self._net

    @net.setter
    def net(self, value):
        self._net = value

    def get_svg_path(self):
        return self.shapely_polygon.svg(self.net.name)


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

    @property
    def x(self) -> float:
        return self.point.x

    @property
    def y(self) -> float:
        return self.point.y


class Net:
    """Тут описаны связи между дорожками и отверстиями"""
    def __init__(self, name: str, start_drill: Drill):
        self.name = name
        self.traces = set()
        self.drills = set()

    def add_drill(self, drill: Drill):
        if drill.net is None:
            drill.net = self
        self.drills.add(drill)

    def add_trace(self, trace: Trace):
        """Добавляет одиночный полигон в цепь"""
        if trace.net is None:
            trace.net = self
        self.traces.add(trace)

    def __repr__(self):
        """Красивое отображение цепи при выводе через print"""
        return f"Net({self.name}, Polygons: {
            len(self.traces)}, Drills: {len(self.drills)})"


class Layer:
    def __init__(self, gerberfile: GerberFile):
        self.gerberfile = gerberfile
        self.traces = []

    def get_traces(self, gerberfile: GerberFile):
        rvmc = gerberfile._get_rvmc()
        shvm = ShapelyVirtualMachine()
        shapely_result = shvm.run(rvmc)
        custom_polygons = [CustomPolygon(geom) for geom in
                           shapely_result.shape.geoms]
        return [Trace(poly) for poly in custom_polygons]


class BoardView:
    def __init__(self,
                 gerber_files: list[GerberFile], drills_file: GerberFile):
        self.gerber_files = gerber_files
        self.drills_file = drills_file
        self.drills = self.get_drill_points(drills_file)
        self.layers = self.make_layers(gerber_files)
        self.net_list = []

    def get_drill_points(self, gerberfile: GerberFile) -> list:
        rvmc = gerberfile._get_rvmc()
        get_drill_vm = GetDrillVirtualMachine()
        get_drill_vm.run(rvmc)
        drills = []
        for point in get_drill_vm.drill_points:
            drills.append(Drill(x=point[0], y=point[1]))
        return drills

    def make_layers(self, gerber_files: list[GerberFile]):
        layers = []
        for gf in gerber_files:
            layers.append(Layer(gf))
        return layers


def print_drill(drill_points):
    print(f"\nНайдено отверстий (D03): {len(drill_points)}")
    for i, (x, y) in enumerate(drill_points, 1):
        print(f"#{i}: X={x}, Y={y}")


# def print_drill_intersects(gerberfile: GerberFile, drill: GerberFile):
#     rvmc = gerberfile._get_rvmc()
#     shvm = ShapelyVirtualMachine()
#     shapely_result = shvm.run(rvmc)
#     polygons = shapely_result.shape.geoms
#     drills = get_drill_points(drill)
#     for i, polygon in enumerate(polygons):
#         for ii, point in enumerate(drills):
#             point = Point(point)
#             if polygon.intersects(point):
#                 print(f"Точка {ii} попала в полигон {i}")


gerber_bot = GerberFile.from_file(BOTTOM_GBR_PATH)
gerber_top = GerberFile.from_file(TOP_GBR_PATH)
gerber_drill = GerberFile.from_file(DRILL_GBR_PATH)

# shapely_image_bot = gerber_bot.render_with_shapely()
# shapely_image_top = gerber_top.render_with_shapely()
# drill_points = get_drill_points(gerber_drill)

# shapely_image_top.save_svg(TOP_SVG_PATH)
# shapely_image_bot.save_svg(BOTTOM_SVG_PATH)

# print_drill_intersects(gerber_top, gerber_drill)
# print_drill_intersects(gerber_bot, gerber_drill)
