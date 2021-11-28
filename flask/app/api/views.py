"""
API routes:

/api/tempo?token=xxx

/api/login?usuario=xxxx&senha=xxxxx

"""


from flask import jsonify, request, Response
from flask_login import current_user

from . import api
from ..models import Usuario, encode_md5
from .. import db
from ..utils import get_mensagens

from typing import Tuple
from dataclasses import dataclass, field
import json
from random import choice
import os


@dataclass
class Response:
    status: int = 200
    d: dict = field(default_factory=dict)

    def pack(self) -> Tuple[Response, int]:
        self.d['status'] = self.status
        response = jsonify(self.d)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, self.status


def generate_token(user: Usuario):
    user.token = encode_md5(str(user.email) + str(user.senha))
    db.session.commit()


@api.route('/api/tempo', methods=['GET'])
def tempo():
    r = Response()

    if request.json:
        args = request.json
    else:
        args = request.args

    token = args.get('token')
    if token is None:
        r.d = {'error': 'token nao encontrado'}
        r.status = 400
        return r.pack()

    # pra testes
    if token == 'teste':
        r.d = {'tempo', 5}
        r.status = 234
        return r.pack()

    u: Usuario = Usuario.query.filter_by(token=token).first()
    if u is None:
        r.d = {'error': 'token invalido'}
        r.status = 400
        return r.pack()

    r.d = {'hora_inicio': u.hora_inicio, 'hora_final': u.hora_fim}
    return r.pack()


@api.route('/api/login', methods=['GET', 'POST'])
def login():
    r = Response()

    if request.json:
        args = request.json
    else:
        args = request.args

    usuario = args.get('usuario')
    senha = args.get('senha')

    if usuario is None or senha is None:
        r.d = {'error': 'usuario e senha nao encontrados'}
        r.status = 400
        return r.pack()

    u: Usuario = Usuario.query.filter_by(email=usuario).first()
    if u is None:
        r.d = {'error': 'email nao encontrado'}
        r.status = 400
        return r.pack()

    if u.senha != senha:
        r.d = {'error': 'senha incorreta'}
        r.status = 401
        return r.pack()

    if u.token is None:
        generate_token(u)

    r.d = {
        'token': u.token,
        'hora_inicio': u.hora_inicio,
        'hora_final': u.hora_fim
    }
    return r.pack()


@api.route("/api/mensagem", methods=['GET', "POST"])
def mensagem():
    ret = {'mensagem': get_mensagens()}
    return jsonify(ret)


@api.route("/api/pontos", methods=["GET", "POST"])
def pontos():
    if not current_user.is_authenticated:
        return jsonify({})

    p = request.args.get('pontos')
    if p is not None and p.isnumeric():
        user: Usuario = current_user
        user.pontos = user.pontos + int(p)
        db.session.add(user)
        db.session.commit()

    return jsonify({})
