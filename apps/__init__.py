# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from importlib import import_module
from apps.config import config_dict

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Setup login manager
login_manager.session_protection = 'strong'
login_manager.login_view = 'authentication_blueprint.login'  # Login sayfasının endpoint'i
login_manager.login_message = 'Lütfen giriş yapınız.'  # Türkçe mesaj
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from apps.authentication.models import Users
    return Users.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('authentication_blueprint.login'))

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

def register_blueprints(app):
    for module_name in ('home', 'authentication'):
        module = import_module(f'apps.{module_name}.routes')
        app.register_blueprint(module.blueprint)

def create_app(config='development'):  # default değeri 'development' olarak değiştirildi
    app = Flask(__name__)
    app.config.from_object(config_dict[config])
    
    register_extensions(app)
    register_blueprints(app)
    
    with app.app_context():
        db.create_all()
    
    return app