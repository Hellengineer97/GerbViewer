from pygerber.gerber.api import GerberFile
from pygerber.vm.shapely import ShapelyVirtualMachine
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
from constant import BOTTOM_GBR_PATH, TOP_GBR_PATH, DRILL_GBR_PATH, TOP_SVG_PATH, BOTTOM_SVG_PATH


class GetDrillVirtualMachine(ShapelyVirtualMachine):
    """Переделанная вирт машина чтобы вытягивать координаты отвертий"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Список будет жить внутри конкретного экземпляра машины
        self.drill_points = []
    def on_paste_layer_eager(self, command):
        # Ловим D03, забираем чистый вектор центра
        self.drill_points.append((command.center.x, command.center.y))
       
class CustomPolygon():
    """Переделанный класс полигона который генерит SVG элемент без лишнего мусора"""
    def __init__(self, poly_object):
        self._poly = poly_object
    def __getattr__(self, name):
        return getattr(self._poly, name)
    
    def svg(self):
        if self.is_empty:
            return "<g />"
            
        exterior_coords = ["{},{}".format(*c) for c in self.exterior.coords]
        interior_coords = [
            ["{},{}".format(*c) for c in interior.coords] for interior in self.interiors
        ]
        
        all_rings = [exterior_coords] + interior_coords
        path_segments = []
        for coords in all_rings:
            if len(coords) > 0:
                path_segments.append(f"M {coords[0]} L {' '.join(coords[1:])} Z")
                
        path = " ".join(path_segments)
        return f'<path tabindex="0" d="{path}" />'


def get_drill_points(gerberfile: GerberFile) -> list:    
    rvmc = gerberfile._get_rvmc()
    get_drill_vm = GetDrillVirtualMachine()
    get_drill_vm.run(rvmc)
    return get_drill_vm.drill_points

def print_drill(drill_points):
    print(f"\nНайдено отверстий (D03): {len(drill_points)}")
    for i, (x, y) in enumerate(drill_points, 1):
        print(f"#{i}: X={x}, Y={y}")

def print_shaperesult(gerberfile: GerberFile):
    rvmc = gerberfile._get_rvmc()
    shvm = ShapelyVirtualMachine()
    shapely_result = shvm.run(rvmc)
    print(shapely_result.shape.svg())

def print_multipol(gerberfile: GerberFile):
    rvmc = gerberfile._get_rvmc()
    shvm = ShapelyVirtualMachine()
    shapely_result = shvm.run(rvmc)
    custom_polygons = [CustomPolygon(geom) for geom in shapely_result.shape.geoms]
    print(custom_polygons[0].svg())

def print_drill_intersects(gerberfile: GerberFile, drill: GerberFile):
    rvmc = gerberfile._get_rvmc()
    shvm = ShapelyVirtualMachine()
    shapely_result = shvm.run(rvmc)
    polygons = shapely_result.shape.geoms
    drills = get_drill_points(drill)
    for i, polygon in enumerate(polygons):
        for ii, point in enumerate(drills):
            point = Point(point)
            if polygon.intersects(point):
                print(f"Точка {ii} попала в полигон {i}")



gerber_bot = GerberFile.from_file(BOTTOM_GBR_PATH)
gerber_top = GerberFile.from_file(TOP_GBR_PATH)
gerber_drill = GerberFile.from_file(DRILL_GBR_PATH)

shapely_image_bot = gerber_bot.render_with_shapely()
shapely_image_top = gerber_top.render_with_shapely()
drill_points = get_drill_points(gerber_drill)

shapely_image_top.save_svg(TOP_SVG_PATH)
shapely_image_bot.save_svg(BOTTOM_SVG_PATH)

print_drill_intersects(gerber_top, gerber_drill)
print_drill_intersects(gerber_bot, gerber_drill)


