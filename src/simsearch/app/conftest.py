import os
import pytest
from app import app, db
from app.models import User, Post
basedir = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def client():
    app.config['TESTING'] = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' # noqa
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'test.db')
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DEBUG'] = False
    client = app.test_client()
    with app.app_context():
        db.drop_all()
        db.create_all()
    create_test_user()

    yield client


@pytest.fixture
def webdriver(request):
    q = db.session.query(User).filter(User.username == 'test1')
    q.delete()
    db.session.commit()
    from selenium import webdriver
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'test.db')
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DEBUG'] = False
    driver = webdriver.Chrome("C:/Users/dovy/chromedriver_win32/chromedriver")
    with app.app_context():
        db.drop_all()
        db.create_all()
    create_test_user()
    request.addfinalizer(driver.quit)
    yield driver


def create_test_user():
    user = User(username='test', email='test@example.com')
    user.set_password("test")
    db.session.add(user)
    p = Post(body='test.jpeg', author=user)
    db.session.add(p)
    user = User(username='testyy', email='testy@example.com')
    user.set_password("testyy")
    db.session.add(user)
    db.session.commit()
