from os import getenv
from app import create_app
# from config import app_config

config_name = getenv('FLASK_ENV', default='development')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
