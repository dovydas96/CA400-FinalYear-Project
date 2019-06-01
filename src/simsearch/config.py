import os
basedir = os.path.abspath(os.path.dirname(__file__))
S3_BUCKET = 'simsearch'
S3_KEY = os.environ.get("AKIAICFLSEVSLOEVKHEQ")
S3_SECRET = os.environ.get("S3_SECRET")


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'no-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
