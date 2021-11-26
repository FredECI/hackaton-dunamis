from typing import Dict
from os import getenv

# para todas as configuracoes:
# https://flask.palletsprojects.com/en/2.0.x/config/

db_postgres = {
    'senha': getenv("POSTGRES_PASSWORD"),
    'host': getenv("POSTGRES_CONNECTION"),
    'user': getenv('POSTGRES_DATABASE'),
}

db_mysql = {
    'senha': getenv('MYSQL_PASSWORD'),
    'host': getenv('MYSQL_CONNECTION'),
    'user': getenv('MYSQL_DATABASE')
}

MYSQL_URI = getenv('MYSQL_URI')

database = 'MYSQL' if db_mysql['user'] is not None else 'POSTGRES'

db = db_mysql if database == 'MYSQL' else 'POSTGRES'


class Config:
    """
    Configurações comuns
    """
    def __init__(self):
        for x, y in db.items():
            if y is None:
                print(f'a variavel de ambiente {x} nao foi definida. abortando...')
                exit(1)

    if MYSQL_URI is not None:
        SQLALCHEMY_DATABASE_URI = MYSQL_URI

    elif database == 'MYSQL':
        SQLALCHEMY_DATABASE_URI = \
            f'mysql://{db["user"]}{":" + db["senha"] if db["senha"] is not None else ""}@{db["host"]}/dev'
    else:
        SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{db["senha"]}@{db["host"]}/{db["user"]}'


class DevelopmentConfig(Config):
    """
    Configurações para desenvolvimento
    """

    DEBUG = True
    SQLACHEMY_ECHO = True   # exibe as operacoes no terminal
    SECRET_KEY = '0uyt7jvp2kjvpgt7oabbjvl513'


class ProductionConfig(Config):
    """
    Configurações para produção
    """

    DEBUG = False


app_config: Dict[str, object] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
