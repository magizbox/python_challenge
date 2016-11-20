import json
from flask import Flask, render_template, request
import os
import flask
from IPython.utils.capture import capture_output

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/level1')
def level1():
    return render_template("level1.html")

@app.route('/badge')
def badge():
    return render_template("badge.html")


@app.route("/execute", methods=["POST"])
def execute():
    try:
        code = request.json['code']
        with capture_output() as c:
            exec code
        result = {"b": "1"}
    except SyntaxError, e:
        result = {"error": "syntax error"}
    finally:
        return flask.jsonify(**result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
