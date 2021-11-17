# flask imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# module imports

# typing and local imports
from typing import Dict


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_object: object):
    """
    Inicialize o app do Flask
    :param config_object: dicionario contendo as configuracoes
    :return: Flask instance
    """

    app = Flask(__name__)
    # configuracao do Flask
    app.config.from_object(config_object)

    # configuracoes do flask_login
    login_manager.init_app(app)
    login_manager.login_message = "Você deve estar logado para acessar essa página"
    login_manager.login_message_category = 'danger'
    # login_manager.login_view = "auth.login"

    # configuracoes da base de dados
    db.init_app(app)

    # configuracoes para erro
    # app.register_error_handler(500, pagina_de_erro)

    # blueprints
    # from .xxx import xxx as xxxx
    # app.register_blueprint(xxx)

    # configuracoes do bootstrap
    # mais sobre bootstrap: https://pythonhosted.org/Flask-Bootstrap/basic-usage.html
    Bootstrap(app)

    # export de alguma funcao para o jinja
    # app.jinja_env.globals.update(xxx=xxx)

    return app
