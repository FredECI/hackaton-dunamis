from flask import render_template

from . import home


@home.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

