import os

from flask import Flask
from dotenv import load_dotenv

from routes import main_bp


def create_app() -> Flask:
    """Application factory for clean, modular Flask setup."""
    load_dotenv()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
    app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB upload limit
    app.config["UPLOAD_FOLDER"] = "uploads"

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.register_blueprint(main_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
