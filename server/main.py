from flask import Flask
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


wsgi = WsgiToAsgi(app)
