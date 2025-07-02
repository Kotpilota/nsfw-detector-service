from flask import Flask

from app.config import Config
from app.endpoints.moderation_endpoints import moderation_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(moderation_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8000)
