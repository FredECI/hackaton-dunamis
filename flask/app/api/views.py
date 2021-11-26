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
        return {'error': 'token nao encontrado'}

    u: Usuario = Usuario.query.filter_by(token=token).first()
    if u is None:
        return {'error': 'token invalido'}

    if not isinstance(u.tempo, int):
        return {'error': 'tempo registrado invalido'}

    return {'tempo': u.tempo}


