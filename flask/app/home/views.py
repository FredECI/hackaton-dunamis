from flask import render_template
from flask_login import login_required

from . import home
from ..models import Usuario


@home.route("/", methods=['GET', 'POST'])
def index():
    return render_template('home/index.html')


@home.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('base.html')


@home.route('/exercise', methods=['GET', "POST"])
def exercise():
    return render_template('api/exercise.html')
