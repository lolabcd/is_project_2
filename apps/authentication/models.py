# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from apps import db, login_manager
from apps.authentication.util import hash_pass

class Role(db.Model):
    __tablename__ = 'Role'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)
    
    # Relationship with Users (one-to-many)
    users = db.relationship('Users', backref='role', lazy=True)


class Report(db.Model):
    __tablename__ = 'Report'
    report_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    report_date = db.Column(db.Date, nullable=False)
    gpt_text = db.Column(db.Text)
    impressions = db.Column(db.Integer)
    reach = db.Column(db.Integer)
    visits = db.Column(db.Integer)
    ads = db.Column(db.Integer) 

    # No need for a self-referential relationship here; link back to Users instead
    user = db.relationship('Users', backref='reports', lazy=True)


class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    role_id = db.Column(db.Integer, db.ForeignKey('Role.role_id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_id(self):
        return str(self.user_id)  # Convert to string for compatibility

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # hash password on init

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


# Remove the duplicate db initialization here

@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(user_id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
