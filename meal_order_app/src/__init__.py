import os
from flask import Flask, jsonify
from src.settings import SQL_URI

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=SQL_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def hello_world():
        return jsonify(hello="world")

    from .api import users, address, payments, items, orders, names, contacts
    app.register_blueprint(users.bp)
    app.register_blueprint(address.bp)
    app.register_blueprint(payments.bp)
    app.register_blueprint(items.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(names.bp)
    app.register_blueprint(contacts.bp)

    return app
