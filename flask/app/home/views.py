from flask import render_template

from . import home
from ..models import Usuario


@home.route("/", methods=['GET', 'POST'])
def index():
    # user = Usuario.query.filter_by(email='daniel@email.com').first()
    return render_template('index.html', nome=user.nome)

