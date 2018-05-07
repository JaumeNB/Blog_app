import os
from dotenv import load_dotenv
APP_DIR = os.path.dirname(os.path.realpath(__file__))

# application imports the variables in this file when it starts
# there is no need to have all these variables manually set by you.
load_dotenv(os.path.join(APP_DIR, '.env'))

# Unfortunately, these environment variables have to be defined
# because these are needed very early in the application bootstrap process

#   export FLASK_APP=blogapp.py
#   export FLASK_DEBUG=1

class Config(object):

    SQLALCHEMY_DATABASE_URI = 'sqlite:////%s' % os.path.join(APP_DIR, 'DB/blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 2
    LANGUAGES = ['en', 'es']
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
