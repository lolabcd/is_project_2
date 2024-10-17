# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)
    
#!!!!SECOND CHANGE !!!!

db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'Role'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)
    
    users = db.relationship('User', backref='role', lazy=True)

class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('Role.role_id'), nullable=False)
    
    social_media_accounts = db.relationship('SocialMediaAccount', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    reports = db.relationship('Report', backref='user', lazy=True)

class SocialMediaAccount(db.Model):
    __tablename__ = 'SocialMediaAccount'
    account_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    access_token = db.Column(db.String(200), nullable=False)
    
    analytics = db.relationship('MetaAccountAnalytics', backref='account', lazy=True)

class Notification(db.Model):
    __tablename__ = 'Notification'
    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

class MetaAccountAnalytics(db.Model):
    __tablename__ = 'MetaAccountAnalytics'
    analytics_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('SocialMediaAccount.account_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    data = db.Column(db.Text, nullable=False)

class Report(db.Model):
    __tablename__ = 'Report'
    report_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    report_date = db.Column(db.Date, nullable=False)
    content = db.Column(db.Text, nullable=False) 

@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
