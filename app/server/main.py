from asgiref.wsgi import WsgiToAsgi
from flask import Flask, render_template
import requests

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)


@app.route("/")
def display_plots():
    url = "http://localhost:8000/"
    response1 = requests.get(f"{url}barchart")
    response2 = requests.get(f"{url}treemap")
    bar = response1.json().get("plot")
    tree = response2.json().get("plot")
    return render_template("index.html", barGraphJSON=bar, treeMapJSON=tree)
