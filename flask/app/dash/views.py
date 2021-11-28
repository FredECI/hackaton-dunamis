from flask import render_template, jsonify
from flask_login import current_user

from . import dash
from .utils import get_scoreboard


@dash.route('/aiyudeygfiosaf', methods=['GET'])
def aiyudeygfiosaf():
    return jsonify(get_scoreboard())
