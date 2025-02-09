# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for, Blueprint
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)

from apps import db
from apps.authentication.forms import CreateAccountForm, LoginForm
from apps.authentication.models import Users
from apps.authentication.util import verify_pass
from werkzeug.security import generate_password_hash

blueprint = Blueprint(
    'authentication_blueprint',
    __name__,
    url_prefix='/auth'
)

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # Formu doğrula
        username = request.form['username']
        password = request.form['password']

        # Kullanıcıyı veritabanında ara
        user = Users.query.filter_by(username=username).first()

        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('home.index'))

        # Hatalı giriş durumunda
        return render_template('accounts/login.html',
                               msg='Yanlış kullanıcı adı veya şifre',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home.index'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']
        
        # Şifreyi hash'le
        password = generate_password_hash(request.form['password'])

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # Hash the password before storing
        user = Users(**{
            'username': username,
            'email': email,
            'password': password,
            'is_superadmin': False
        })

        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        return render_template('accounts/register.html',
                               msg='User created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index')) 

# Errors

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
