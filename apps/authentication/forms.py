# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired

## login and registration forms
class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Şifre',
                           id='pwd_login',
                           validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    username = StringField('Kullanıcı Adı',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Şifre',
                         id='pwd_create',
                         validators=[DataRequired()])
