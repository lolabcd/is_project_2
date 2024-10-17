import os
import logging
import pymysql

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from importlib import import_module

pymysql.install_as_MySQLdb() 
db = SQLAlchemy()
login_manager = LoginManager()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        try:
            # Attempt to connect to MySQL/MariaDB
            db.create_all()
        except Exception as e:
            app.logger.error('DBMS Exception: %s', str(e))

            # Fallback to SQLite if MySQL connection fails
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
            app.logger.info('Fallback to SQLite')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Set up MySQL/MariaDB URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3311/isproject'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, for performance

    register_extensions(app)
    register_blueprints(app)
    configure_database(app)

    return app
