from flask import render_template, jsonify
from flask_login import current_user

from . import dash
from .utils import get_scoreboard


@dash.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('home/index.html')
