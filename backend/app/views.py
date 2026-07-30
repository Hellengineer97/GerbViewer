from flask import render_template

from app import app
from boardview import Boardview

boardview: Boardview | None = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/get-svg')
def get_svg():
    if boardview is not None:
        return render_template('none.svg')
    return render_template('none.svg')
