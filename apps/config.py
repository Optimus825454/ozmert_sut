# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Set up SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql://bborsa:518518@localhost/cybetpunkt_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Login config
    SECRET_KEY = '518518Erkan'
    
    # Session config
    SESSION_COOKIE_SECURE = False  # Development için False
    SESSION_COOKIE_HTTPONLY = True

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # Production'da True olmalı

class DebugConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # Development'da False

# Konfigürasyon dictionary'si
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig,
    'development': DebugConfig
}
