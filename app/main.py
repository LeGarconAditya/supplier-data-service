from flask import Flask


def create_app():
    app = Flask(__name__)
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
