import os

from config import Config

from flask import Flask


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # db.init_app(app)
    # migrate.init_app(app)

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        if not os.path.exists("logs"):
            os.mkdir("logs")

    return app
