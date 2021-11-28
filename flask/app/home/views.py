from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user, login_user

from . import home
from ..models import Usuario, Tempo, Pergunta, Resposta
from .. import db
from ..api.views import generate_token

from datetime import datetime, timedelta
from typing import List


@home.route("/", methods=['GET', 'POST'])
def index():
    return render_template('home/index.html')


@home.route('/exercise', methods=['GET', "POST"])
def exercise():
    token = request.args.get('token')
    timing = request.args.get('tempo')
    # print('token', token)
    if token is not None:
        user: Usuario = Usuario.query.filter_by(token=token).first()
        # print("achei um usario: ", user)
        if user is None:
            # print("usuario none :(")
            return redirect(url_for('home.index'))

        login_user(user)
        if timing is not None:
            return redirect(url_for('home.exercise', tempo=timing))
        return redirect(url_for('home.exercise'))

    else:
        if not current_user.is_authenticated:
            return redirect(url_for('home.index'))

        user: Usuario = current_user
        token = user.token

    # verificando se pode entrar nessa hora
    hora_min = user.hora_inicio
    hora_max = user.hora_fim
    datetime_now = datetime.now()
    hora_now = datetime_now.hour
    print(hora_now, hora_max, hora_min)
    if not (hora_min <= hora_now < hora_max):
        return render_template(
            'home/exercise-page.html', duracao_min=0, duracao_seg=0,
            ja_comecou=False,
            mensagem="Não é a hora programada ainda. Volte novamente mais tarde (%02d:00 - %02d:00)" %
                     (hora_min, hora_max))

    # pegando o tempo antigo
    duracao_min = request.args.get('tempo', '10')
    duracao_seg = 0
    if not duracao_min.isnumeric():     # NaN
        # print("duracao invalida")
        return redirect(url_for('home.index'))
    else:
        duracao_min = int(duracao_min)

    tempo: Tempo = Tempo.query.filter_by(token=token).first()
    ja_comecou = False
    # se nao tiver tempo anterior
    if tempo is None or tempo.hora is None:
        if tempo is None:
            tempo = Tempo()

        tempo.token = token
        tempo.hora = datetime_now.isoformat()

        # print(tempo.token, tempo.hora)
        db.session.add(tempo)
        db.session.commit()

    # com tempo anterior, tem que verificar
    else:
        hora_banco_str: str = tempo.hora
        hora_banco: datetime = datetime.fromisoformat(hora_banco_str)
        hora_atual: datetime = datetime_now
        diff: timedelta = hora_atual - hora_banco
        diff_sec = diff.seconds % 3600
        if diff_sec > duracao_min * 60:  # era antigo, reset
            tempo.token = token
            tempo.hora = hora_atual.isoformat()

            user.quantidade = user.quantidade + 1
            db.session.add(user)
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


@home.route("/pesquisa", methods=['GET', "POST"])
@login_required
def pesquisa():
    user: Usuario = current_user

    if request.method == 'POST':
        token = user.token

        # limpando as pesquisas anteriores
        Resposta.query.filter_by(token_pessoa=token).delete()

        # colocando as respostas novas
        for entradas in request.form:
            # print(entradas)
            id_pergunta = entradas.lstrip('input-')
            if id_pergunta.isnumeric():
                r = Resposta()
                r.token_pessoa = token
                r.id_pergunta = int(id_pergunta)
                r.ident = r.token_pessoa + str(r.id_pergunta)
                db.session.add(r)

        db.session.commit()
        return render_template('home/obrigado.html')

    perguntas: List[Pergunta] = Pergunta.query.all()

    if user.genero.lower() == 'm':
        dict_perguntas = {
            o.id: o.texto for o in perguntas if o.categoria.lower() != 'filho'
        }
    else:
        dict_perguntas = {
            o.id: o.texto for o in perguntas
        }

    return render_template('home/form-page.html', perguntas=dict_perguntas)

