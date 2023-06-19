import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a5b88d557bee98d2b8ab356b01d6f41e'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'mysql://u2105133_mysql:swordfish1@localhost:3306/u2105133_mysql'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    @staticmethod
    def init_app(app):
        pass

    @staticmethod
    def create_db():
        from sqlalchemy import create_engine
        from sqlalchemy_utils import database_exists, create_database
    
        if os.environ.get('DATABASE_URL') != None:
            engine = create_engine(os.environ.get('DATABASE_URL'))
            if not database_exists(engine.url):
                create_database(engine.url)
            print(database_exists(engine.url))
            return create_database

class DevelopmentConfig(Config):
    DEBUG = True
    Config.create_db()    
    
class ProductionConfig(Config):
    DEBUG = False
    Config.create_db() 

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}