import os


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config(object):
    FLASK_WEB_NAME = '工具集合管理平台'
    SECRET_KEY = os.environ.get('SECRET_KEY') or '!@#$AB%^&*12345678dDK*'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    POST_PRE_PAGE = 20
    WTF_I18N_ENABLED = False

    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/12'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
