from os import environ
from importlib import import_module

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .key import get_key

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    import_module("app.models")
    db.init_app(app)
    migrate.init_app(app, db)

    app.config['SECRET_KEY'] = get_key()

    app.config['PROJECT_MAX'] = 100
    app.config['DEPLOY_MAX'] = 80

    from . import views
    for view in [getattr(views, x) for x in views.__all__]:
        app.register_blueprint(view.bp)

    from .error import RedirectRequired
    from .error import handle_redirect_required
    app.register_error_handler(RedirectRequired, handle_redirect_required)

    return app
