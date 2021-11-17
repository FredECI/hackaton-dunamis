from os import getenv
from app import create_app
from config import app_config

if __name__ == '__main__':
    app = create_app(app_config.get(getenv('FLASK_ENV')))
    app.run()
