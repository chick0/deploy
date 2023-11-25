from os import environ
from sys import argv
from importlib import import_module

from flask import g
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix

from .const import VERSION
from .key import get_key

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
    )

    if "--dev" in argv:
        app.jinja_options = {
            "cache_size": 0
        }

    if "--sql-echo" in argv:
        app.config["SQLALCHEMY_ECHO"] = True

    import_module("app.models")
    db.init_app(app)
    migrate.init_app(app, db)

    app.config['SECRET_KEY'] = get_key()

    @app.before_request
    def before_request():
        g.VERSION = VERSION

    from . import views
    for view in [getattr(views, x) for x in views.__all__]:
        app.register_blueprint(view.bp)

    from . import tools
    app.add_template_filter(tools.size2str)

    from . import error
    app.register_error_handler(404, error.handle_404)

    return app
