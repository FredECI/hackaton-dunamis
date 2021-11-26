import os
from abc import ABC

from gunicorn.app.base import Application
from app import create_app
from config import app_config


class FlaskAPP(Application, ABC):
    def __init__(self):
        super().__init__()

    def load(self):
        config_name = os.getenv('FLASK_ENV', 'development')
        _app = create_app(config_name)
        return _app


if __name__ == '__main__':
    a = FlaskAPP()
    a.run()
