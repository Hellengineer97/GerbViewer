"""
Шрагалка по типам слев
            TopSide      (SilkTop
                        PadsTop
                        CuTop
            InnerLayers  list[Cu]
            BottomSiede (CuBottom
                        PadsBottom
                        SilkBottom)
                        Vias
"""
from flask import Flask, Response, json, request
from flask_cors import CORS
from gerbviewlib.boardview import BoardView
from gerbviewlib.boardview.layer import (CuLayer,
                                         PadsLayer,
                                         SilkLayer,
                                         ViasLayer)
from gerbviewlib.renderer import Renderer
from gerbviewlib.net_generator import NetGenerator


app = Flask(__name__)
CORS(app, origins="http://localhost:8000")


@app.route('/render', methods=['POST'])
def render_route():
    files_map = {f.filename: f for f in request.files.getlist(
        'files') if f.filename}
    boardview = BoardView()
    for filename_type_meta in json.loads(request.form.get('metadata') or '[]'):
        filename = filename_type_meta.get('filename')
        layer_type = filename_type_meta.get('type')
        if not layer_type:
            continue
        if file_obj := files_map.get(filename):
            file_str = file_obj.read().decode()
            if not file_str or not file_str.strip():
                continue
            if layer_type == "SilkTop":
                boardview.textolite.top_layer.silk = SilkLayer(
                    gerber_source=file_str)
            elif layer_type == "PadsTop":
                boardview.textolite.top_layer.pads = PadsLayer(
                    gerber_source=file_str)
            elif layer_type == "CuTop":
                boardview.textolite.top_layer.cu = CuLayer(
                    gerber_source=file_str)
            elif layer_type == "Cu":
                boardview.textolite.inner_cu_layers.cu_layers.append(CuLayer(
                    gerber_source=file_str))
            elif layer_type == "CuBottom":
                boardview.textolite.bottom_layer.cu = CuLayer(
                    gerber_source=file_str)
            elif layer_type == "PadsBottom":
                boardview.textolite.bottom_layer.pads = PadsLayer(
                    gerber_source=file_str)
            elif layer_type == "SilkBottom":
                boardview.textolite.bottom_layer.silk = SilkLayer(
                    gerber_source=file_str)
            elif layer_type == "Vias":
                boardview.textolite.vias = ViasLayer(
                    gerber_source=file_str)
    boardview.renderer = Renderer()
    boardview.net_generator = NetGenerator()
    return Response(boardview.render_svg(), mimetype='image/svg+xml')


@app.route('/generate_net', methods=['POST'])
def generate_net_route():
    return Response("Net generation completed.", mimetype='image/svg+xml')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
