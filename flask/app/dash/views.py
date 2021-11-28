from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from . import dash
from ..utils import get_scoreboard, get_empregados, get_gestores, get_doencas


@login_required
@dash.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not current_user.is_authenticated or current_user.gestor != 1:
        return redirect(url_for("home.index"))

    melhores_usuarios = [
        (i, k, v) for i, (k, v) in enumerate(get_scoreboard().items())
    ]

    doencas_mais_comuns = [
        (i, k, v) for i, (k, v) in enumerate(get_doencas().items())
    ][:5]

    quantidade_empregados = get_empregados()

    quantidade_gestores = get_gestores()

    return render_template('dash/dashboard-gestor.html',
                           melhores_usuarios=melhores_usuarios,
                           doencas_mais_comuns=doencas_mais_comuns,
                           quantidade_empregados=quantidade_empregados,
                           quantidade_gestores=quantidade_gestores)


