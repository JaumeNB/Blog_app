"""IMPORTS"""
import os
import logging
from flask import Flask, request, send_from_directory, Markup, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy import MetaData
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from flask_ckeditor import CKEditor

#necessary to make database migration work
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

"""FLASK APP INITIALIZATION"""
#create an instance (object) of the Flask class
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
app.config['UPLOADED_PATH'] = basedir + '/uploads'
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 600
app.config['CKEDITOR_PKG_TYPE'] = 'full'

"""FLASK LOGIN"""
login = LoginManager(app)
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')

"""CONFIGURATION FILE"""
app.config.from_object(Config)

"""DATABASE INITIALIZATION"""
db = SQLAlchemy(app, metadata=MetaData(naming_convention=naming_convention))

"""DATABASE MIGRATION"""
migrate = Migrate(app, db)

"""TIME FORMAT HANDLING"""
moment = Moment(app)

"""SUPPORT FOR MULTIPLE LANGUAGES"""
babel = Babel(app)

"""SUPPORT CKEDITOR"""
ckeditor = CKEditor(app)

"""LOG ERRORS"""
if not app.debug:

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/blogapp.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('blogapp startup')

"""MATCH PREFERED LANGUAGE TO SUPPORTED LANGUAGES"""
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

"""IMPORTS TO AVOID CATCH 22 IMPORT ISSUE"""
from app import routes, models, errors
