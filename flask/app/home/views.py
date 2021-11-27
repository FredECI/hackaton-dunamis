from flask import render_template
from flask_login import login_required

from . import home
from ..models import Usuario


@home.route("/", methods=['GET', 'POST'])
def index():
    # user = Usuario.query.filter_by(email='daniel@email.com').first()
    return render_template('base.html')


@login_required
@home.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('base.html')

