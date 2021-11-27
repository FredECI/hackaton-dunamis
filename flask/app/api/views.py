"""
API routes:

/api/tempo?token=xxx

/api/login?usuario=xxxx&senha=xxxxx

"""


from flask import jsonify, request, current_app, Response

from . import api
from ..models import Usuario, encode_md5
from .. import db


def generate_token(user: Usuario):
    user.token = encode_md5(str(user.email) + str(user.senha))
    db.session.commit()


@api.route('/api/tempo', methods=['GET'])
def tempo():
    token = request.args.get('token')
    if token is None:
        return jsonify({'error': 'token nao encontrado'}), 400

    # pra testes
    if token == 'teste':
        return jsonify({'tempo': 5})

    u: Usuario = Usuario.query.filter_by(token=token).first()
    if u is None:
        return jsonify({'error': 'token invalido'}), 400

    if not isinstance(u.tempo, int):
        return {'error': 'tempo registrado invalido'}, 500

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
        return {'error': 'tempo registrado invalido'}, 500

    if u.token is None:
        generate_token(u)

    return jsonify({
        'token': u.token,
        'tempo': u.tempo
    })

