import os
APP_DIR = os.path.dirname(os.path.realpath(__file__))

#set in V environment:
#   export FLASK_APP=blogapp.py
#   export FLASK_DEBUG=1

class Config(object):

    SECRET_KEY = 'supercalifragilisticoespialidoso'   # Used by Flask to encrypt session cookie.
    SQLALCHEMY_DATABASE_URI = 'sqlite:////%s' % os.path.join(APP_DIR, 'DB/blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 2
    LANGUAGES = ['en', 'es']
