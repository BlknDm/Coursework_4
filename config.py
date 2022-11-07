class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///kino.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PER_PAGE = 12
