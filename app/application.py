from flask import Flask
from app.controller import assistant_controller

app = Flask(__name__)
app.register_blueprint(assistant_controller)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)