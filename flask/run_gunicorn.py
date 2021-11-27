import os

from gunicorn.app.base import Application
import app


class FlaskAPP(Application):
    def __init__(self):
        super().__init__()

    def init(self, parser, opts, args):
        path = os.path.join(os.getcwd(), 'flask', 'gunicorn.conf.py')
        self.load_config_from_module_name_or_filename(path)

    def load(self):
        config_name = os.getenv('FLASK_ENV', 'development')
        return app.create_app(config_name)


if __name__ == '__main__':
    _app = FlaskAPP()
    _app.run()
