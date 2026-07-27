# app.py — replaces the HO4 version in flask_coursemanager/app.py
from flask import Flask
from flask_migrate import Migrate
from config import Config
from extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    from courses.routes import courses_bp
    app.register_blueprint(courses_bp)

    @app.errorhandler(404)
    def not_found(e):
        return {"status": "error", "message": "Resource not found"}, 404

    @app.errorhandler(500)
    def server_error(e):
        return {"status": "error", "message": "Internal server error"}, 500

    return app


if __name__ == "__main__":
    create_app().run(port=5000)

# Setup commands:
#   flask db init
#   flask db migrate -m "initial schema"
#   flask db upgrade
