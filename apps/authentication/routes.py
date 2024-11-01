# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import flash, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from wtforms import PasswordField


from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Role, Users
from werkzeug.security import generate_password_hash  
from apps.authentication.util import verify_pass


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']
        bio = request.form.get('bio')
        password = request.form['password'] 
        #role_name = request.form.get('role')  # Get role from form

        # Check if username exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check if email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)
        
        # Find role ID based on role_name
       # role = Role.query.filter_by(role_name=role_name).first()
       # if not role:
            #flash("Invalid role selected")
            #return render_template('accounts/register.html',
                                   #msg='Invalid role',
                                   #success=False,
                                   #form=create_account_form)

        # Create new user with the role

        # Capture additional fields from the form
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        # Hash the password and create a new user
        hashed_password = generate_password_hash(password, method='sha256')
        user = Users(
            username=username,
            email=email,
            bio=bio,
            password=hashed_password, # Store the hashed password
            first_name=first_name,  
            last_name=last_name, 
        )

        # Add user to database
        db.session.add(user)
        db.session.commit()
        
        # Redirect based on role
       # if role_name == "Admin":
           # return redirect(url_for('admin_blueprint.dashboard'))  # Admin dashboard route
      #  else:
      #      return redirect(url_for('home_blueprint.index'))  # Regular user page

    
        # Delete user from session
        logout_user()
        
        return render_template('accounts/register.html',
                               msg='Account created successfully.',
                               success=True,
                               form=create_account_form)
    
    

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
