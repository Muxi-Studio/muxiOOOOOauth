# coding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from celery import Celery
from flask_mail import Mail
# from flask_debugtoolbar import DebugToolbarExtension
from config import config

app = Flask(__name__)
"""
config
 -- 'default': DevelopmentConfig
 -- 'develop': DevelopmentConfig
 -- 'testing': TestingConfig
 -- 'production': ProductionConfig
    you can edit this in config.py
"""
config_name = 'default'
app.config.from_object(config[config_name])
config[config_name].init_app(app)
# toolbar = DebugToolbarExtension(app)
mail = Mail(app)

"""celery config"""
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


# admin site
from admin import views


"""
blueprint
you can register a <blueprint> by run:
 -- mana blueprint <blueprint>
under app folder
"""
from main import main
app.register_blueprint(main, url_prefix='/main')

from auth import auth
app.register_blueprint(auth, url_prefix="/auth")

from api import api
app.register_blueprint(api, url_prefix="/api")

