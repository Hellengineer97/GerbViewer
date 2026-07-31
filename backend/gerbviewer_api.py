from flask import Flask, Response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="http://localhost:8000")


def _parse_request_items():
    files = request.files.getlist('files')
    types = request.form.getlist('types')
    items = []

    for file_obj, layer_type in zip(files, types):
        items.append((file_obj.filename, layer_type or 'unknown'))

    return items


def _build_svg(items, endpoint_name):
    svg_lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'viewBox="0 0 800 220" width="800" height="220">',
        '  <rect width="100%" height="100%" fill="#111"/>',
        '  <text x="20" y="32" fill="#fff" font-size="20">'
        f'Endpoint: {endpoint_name}</text>',
        '  <text x="20" y="60" fill="#ccc" font-size="14">'
        'Uploaded files and parameters:</text>',
    ]

    if not items:
        svg_lines.append(
            '  <text x="20" y="100" fill="#f88" font-size="16">'
            'No files were uploaded.</text>'
        )
    else:
        for index, (filename, layer_type) in enumerate(items, start=1):
            y = 70 + index * 20
            svg_lines.append(
                f'  <text x="20" y="{y}" fill="#aad" font-size="14">'
                f'{index}. {filename} — {layer_type}</text>'
            )

    svg_lines.append('</svg>')
    return '\n'.join(svg_lines)


@app.route('/render', methods=['POST'])
def render_route():
    items = _parse_request_items()
    svg_text = _build_svg(items, 'render')
    return Response(svg_text, mimetype='image/svg+xml')


@app.route('/generate_net', methods=['POST'])
def generate_net_route():
    items = _parse_request_items()
    svg_text = _build_svg(items, 'generate_net')
    return Response(svg_text, mimetype='image/svg+xml')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
