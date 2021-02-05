import os



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'
    SQLALCHEMY_DATABASE_URI = 'mysql://ka7612:123456@zanner.org.ua:33321/ka7612'
    SQLALCHEMY_TRACK_MODIFICATIONS = False



