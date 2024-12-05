import os

class DevelopmentConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'cd8cbabe8c9e4556acb3786fd8389b9b961e8a4f3b34e4748a6a8d4b97c7d4e1')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:placeholder@localhost/factory_management_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class TestingConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'cd8cbabe8c9e4556acb3786fd8389b9b961e8a4f3b34e4748a6a8d4b97c7d4e1')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
