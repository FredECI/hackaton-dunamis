"""
API routes:

/api/tempo?token=xxx

/api/login?usuario=xxxx&senha=xxxxx

"""


from flask import jsonify, request, current_app

from . import api
from ..models import Usuario


@api.route('/api/tempo', methods=['GET'])
def tempo():
    token = request.args.get('token')
    if token is None:
        return jsonify({'error': 'token nao encontrado'})

    # pra testes
    if token == 'teste':
        return jsonify({'tempo': 5})

    u: Usuario = Usuario.query.filter_by(token=token).first()
    if u is None:
        return jsonify({'error': 'token invalido'})

    if not isinstance(u.tempo, int):
        return {'error': 'tempo registrado invalido'}

    return jsonify({'tempo': u.tempo})


@api.route('/api/login', methods=['GET'])
def login():
    usuario = request.args.get('usuario')
    senha = request.args.get('senha')

    if usuario is None or senha is None:
        return jsonify({'error': 'usuario e senha nao encontrados'})

    u: Usuario = Usuario.query.filter_by(email=usuario).first()
    if u is None:
        return jsonify({'error': 'email nao encontrado'})

    if u.senha != senha:
        return jsonify({'error': 'senha incorreta'})

    if not isinstance(u.tempo, int):
        return {'error': 'tempo registrado invalido'}

    return jsonify({'tempo': u.tempo})

