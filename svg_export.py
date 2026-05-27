from constant import (BOTTOM_GBR_PATH, TOP_GBR_PATH, DRILL_GBR_PATH,
                      CU5_GBR_PATH, TRACES_SVG_PATH, BOARDVIEW_SVG_PATH)
from pygerber.gerber.api import GerberFile
from Boardview import BoardView



def CreateBoardViewSvg():

    svg_boardview =''
    svg_head = """
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
        viewBox="0.0 0.0 144.0 280.0" preserveAspectRatio="xMinYMin meet">
        <style>
            svg path {
                transition: fill 0.1s ease;
            }
            g path {
                opacity: 0.6
            }
    """
    svg_net_focus_css = ''
    svg_net_fill_css = ''
    svg_layers_css = """
    .layer1 path{
                fill: red;
            }
            .layer2 path{
                fill: green;
            }
            .layer3 path{
                fill: Gray;
            }
            .layer4 path{
                fill: Blue;
            }
    """
    svg_canvas_head="""
        </style>
        <g transform="matrix(1,0,0,-1,0,280.0)" class="layer1">
    """
    svg_body=''
    svg_end = """
        </g>
    </svg>
    """
    gerber_bot = GerberFile.from_file(BOTTOM_GBR_PATH)
    gerber_top = GerberFile.from_file(TOP_GBR_PATH)
    gerber_cu5 = GerberFile.from_file(CU5_GBR_PATH)
    gerber_drill = GerberFile.from_file(DRILL_GBR_PATH)

    boardview = BoardView(
        [gerber_bot, gerber_top, gerber_cu5, gerber_drill], gerber_drill)

    net_focus = []
    for net in boardview.nets.values():
        net_focus.append(f".{net.name}:focus")

    focus_line = ",\n        ".join(net_focus)

    svg_net_focus_css += f"{focus_line} {{outline: none;}}"
    
    net_fill = []
    for net in boardview.nets.values():
        net_fill.append(f" svg:has(.{net.name}:focus) .{net.name}")

    fill_line = ",\n        ".join(net_fill)

    svg_net_fill_css += f"{fill_line} {{fill: orange;}}" 

    for i, layer in enumerate(boardview.layers):
        layer_class = f"layer{i+1}"   # layer1, layer2, layer3...
            
        svg_body += f'    <g class="{layer_class}">\n'
            
        for trace in layer.traces:
            if trace.net:
                    # Убеждаемся, что класс net правильный
                path_svg = trace.get_svg_path()
            else:
                # Если вдруг net не назначен
                path_svg = trace.get_svg_path().replace('class="', 'class="net0 ')
                
            svg_body += "        " + path_svg + "\n"
            
        svg_body += '    </g>\n'


    svg_boardview+=svg_head+'\n'
    svg_boardview+=svg_net_focus_css+'\n'
    svg_boardview+=svg_net_fill_css+'\n'
    svg_boardview+=svg_layers_css+'\n'
    svg_boardview+=svg_canvas_head+'\n'
    svg_boardview+=svg_net_focus_css+'\n'
    svg_boardview+=svg_body+'\n'
    svg_boardview+=svg_end+'\n'


    with open(BOARDVIEW_SVG_PATH, 'w', encoding='utf-8') as f:
            f.write(svg_boardview)
    print(f"SVG сохранён: {BOARDVIEW_SVG_PATH}")
    
CreateBoardViewSvg()