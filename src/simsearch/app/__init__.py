from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from logging.config import dictConfig
from flask.logging import default_handler
from app.filters import datetimeformat
import os

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.logger.removeHandler(default_handler)
app.config.from_object(Config)
app.jinja_env.filters['datetimeformat'] = datetimeformat
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)
S3_BUCKET = 'simsearch'
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")

from app import routes, models, errors # noqa
