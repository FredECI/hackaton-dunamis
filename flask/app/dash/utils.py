from ..models import Usuario
from .. import db


from typing import Dict


def get_scoreboard() -> Dict[str, int]:
    users = db.session.query(
        Usuario.nome,
        Usuario.pontos
    ).order_by(
        Usuario.pontos.desc()
    ).limit(
        7
    ).all()

    pior: Usuario = db.session.query(
        Usuario.pontos
    ).order_by(
        Usuario.pontos.asc()
    ).first()

    if pior is None:
        pior_pontuacao = -500
    else:
        pior_pontuacao = pior.pontos

    return {
        u.nome: - (pior_pontuacao - u.pontos) for u in users
    }




