from flask import Flask
from src.adapters.http.routes import bp
from src.config import APP_URL, APP_PORT

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host=APP_URL, port=int(APP_PORT))