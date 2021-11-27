import os

from gunicorn.app.base import Application
import app


class FlaskAPP(Application):
    def __init__(self):
        super().__init__()

    def init(self, parser, opts, args):
        self.load_config_from_module_name_or_filename('gunicorn.conf.py')

    def load(self):
        config_name = os.getenv('FLASK_ENV', 'development')
        return app.create_app(config_name)


if __name__ == '__main__':
    _app = FlaskAPP()
    _app.run()
