from flask import render_template

from app import app

boardview = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/get-svg')
def get_svg():
    return render_template('none.svg')
