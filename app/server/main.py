from asgiref.wsgi import WsgiToAsgi
from flask import Flask, render_template
import requests

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)


@app.route("/")
def hello_world():
    url = "http://localhost:8000/"
    response = requests.get(url)
    message = response.json().get("message")
    return render_template("index.html", api_call=message)
