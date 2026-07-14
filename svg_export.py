from constant import (BOTTOM_GBR_PATH, TOP_GBR_PATH, DRILL_GBR_PATH,
                      CU5_GBR_PATH, TRACES_SVG_PATH, BOARDVIEW_SVG_PATH)
from pygerber.gerber.api import GerberFile
from Boardview import BoardView



def CreateBoardViewSvg():

    svg_boardview = ''
    svg_head = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="{0:.1f} {1:.1f} {2:.1f} {3:.1f}" preserveAspectRatio="xMinYMin meet">
    <script type="text/javascript" xlink:href="svg-pan-zoom.min.js"></script>
    <script xlink:href="script.js"></script>
    <style>@import url("styles.css");</style>
    <g transform="matrix(1,0,0,-1,0,0)" class="layer1">
"""
    svg_body = ''
    svg_end = """
    </g>
</svg>
"""
    slot72layer1 = GerberFile.from_file("gbr_source/layer1.gbr")
    slot72layer2 = GerberFile.from_file("gbr_source/layer2.gbr")
    slot72layer3 = GerberFile.from_file("gbr_source/layer3.gbr")
    slot72layer4 = GerberFile.from_file("gbr_source/layer4.gbr")
    slot72layer5 = GerberFile.from_file("gbr_source/layer5.gbr")
    slot72layer6 = GerberFile.from_file("gbr_source/layer6.gbr")
    slot72layer7 = GerberFile.from_file("gbr_source/layer7.gbr")
    slot72layer8 = GerberFile.from_file("gbr_source/layer8.gbr")
    Top = GerberFile.from_file("gbr_source/Bottom_copper_top.gbr")
    Bottom = GerberFile.from_file("gbr_source/Top_copper_top.gbr")
    drillgergber = GerberFile.from_file("gbr_source/drills_copper_top.gbr")

    boardview = BoardView([
         Top,
         Bottom,
         slot72layer1, 
         slot72layer2,
         slot72layer3,
         slot72layer4,
         slot72layer5,
         slot72layer6,
         slot72layer7,
         slot72layer8,
         drillgergber], 
         drillgergber)

    for i, layer in enumerate(boardview.layers):
        layer_class = f"layer{i+1}"
        svg_body += f'    <g class="{layer_class}">\n'
        for trace in layer.traces:
            path_svg = trace.get_svg_path()
            svg_body += "        " + path_svg + "\n"
        svg_body += '    </g>\n'
    
    svg_head = svg_head.format(boardview.bounds.min_x, 
                               boardview.bounds.min_y, 
                               boardview.bounds.width, 
                               boardview.bounds.height)

    svg_boardview+=svg_head+'\n'
    svg_boardview+=svg_body+'\n'
    svg_boardview+=svg_end+'\n'


    with open(BOARDVIEW_SVG_PATH, 'w', encoding='utf-8') as f:
            f.write(svg_boardview)
    print(f"SVG сохранён: {BOARDVIEW_SVG_PATH}")
    
CreateBoardViewSvg()