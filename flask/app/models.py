from flask_login import UserMixin
from sqlalchemy import Column, String, Boolean, Integer
# from flask_login import LoginManager


from hashlib import md5

from . import db, login_manager


def encode_md5(texto: str) -> str:
    return md5(texto.encode()).digest().hex()


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'

    email = Column(String(60), primary_key=True)
    nome = Column(String(120))
    senha = Column(String(128))
    admin = Column(Boolean, default=False)
    gestor = Column(String(50))
    tempo = Column(Integer)
    token = Column(String(100))

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return True  # se pode fazer login

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return f'<Usuario :{self.nome}>'


@login_manager.user_loader
def load_user(pk_email):
    return Usuario.query.get(pk_email)
