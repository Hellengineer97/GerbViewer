from pygerber.gerber.api import GerberFile
from pygerber.vm.shapely import ShapelyVirtualMachine
from constant import BOTTOM_GBR_PATH, TOP_GBR_PATH, DRILL_GBR_PATH


class GetDrillVirtualMachine(ShapelyVirtualMachine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Список будет жить внутри конкретного экземпляра машины
        self.drill_points = []
    def on_paste_layer_eager(self, command):
        # Ловим D03, забираем чистый вектор центра
        self.drill_points.append((command.center.x, command.center.y))
       

def get_drill_points(gerberfile: GerberFile) -> list:    
    rvmc = gerberfile._get_rvmc()
    get_drill_vm = GetDrillVirtualMachine()
    get_drill_vm.run(rvmc)
    return get_drill_vm.drill_points

gerber_bot = GerberFile.from_file(BOTTOM_GBR_PATH)
gerber_top = GerberFile.from_file(TOP_GBR_PATH)
gerber_drill = GerberFile.from_file(DRILL_GBR_PATH)

shapely_image_bot = gerber_bot.render_with_shapely()
shapely_image_top = gerber_top.render_with_shapely()
drill_points = get_drill_points(gerber_drill)

print(f"\nНайдено отверстий (D03): {len(drill_points)}")
for i, (x, y) in enumerate(drill_points, 1):
    print(f"#{i}: X={x}, Y={y}")