# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField
from wtforms.validators import Email, DataRequired


# login and registration


class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    role = SelectField('Role', choices=[('socialmediamanager', 'Social media manager'), ('admin', 'Admin')], validators=[DataRequired()])
    bio =  StringField('Bio', validators=[DataRequired()])
   