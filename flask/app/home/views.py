from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from . import home
from ..models import Usuario, Tempo
from .. import db

from datetime import datetime, timedelta


@home.route("/", methods=['GET', 'POST'])
def index():
    return render_template('home/index.html')


@home.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('base.html')


@home.route('/exercise', methods=['GET', "POST"])
def exercise():
    if current_user.is_authenticated():
        token = current_user.token
    else:
        token = request.args.get('token')
        if token is not None:
            return redirect(url_for('home.index'))
        if Usuario.query.filter_by(token=token).first() is not None:
            return redirect(url_for('home.index'))

    duracao_min = request.args.get('tempo', '10')
    duracao_seg = 0
    if not duracao_min.isnumeric():     # NaN
        return redirect(url_for('home.index'))
    else:
        duracao_min = int(duracao_min)

    tempo: Tempo = Tempo.query.filter_by(token=token).first()
    ja_comecou = False

    if tempo is None or tempo.hora is None:
        if tempo is None:
            tempo = Tempo()
            tempo.token = token
        tempo.hora = datetime.now().isoformat()

        db.session.add(tempo)
        db.session.commit()

    else:
        hora_banco_str: str = tempo.hora
        hora_banco: datetime = datetime.fromisoformat(hora_banco_str)
        hora_atual: datetime = datetime.now()
        diff: timedelta = hora_atual - hora_banco
        diff_sec = diff.seconds % 3600
        if diff_sec > duracao_min * 60:  # era antigo, reset
            tempo.hora = hora_atual.isoformat()
            db.session.add(tempo)
            db.session.commit()
        else:   # tempo correndo ainda
            ja_comecou = True
            duracao_seg = duracao_min * 60 - diff_sec
            duracao_min = duracao_seg // 60
            duracao_seg %= 60

    return render_template('home/exercise-page.html',
                           duracao_min=duracao_min, duracao_seg=duracao_seg,
                           ja_comecou=ja_comecou)
