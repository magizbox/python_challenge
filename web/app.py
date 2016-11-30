from __future__ import with_statement
import traceback
from flask import Flask, render_template, request
import os
import flask
from IPython.utils.capture import capture_output

from manager import time_limit, TimeoutException

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("index.html")


@app.route('/level1')
def level1():
    return render_template("level1.html")

@app.route('/level1_answer')
def level1_answer():
    return render_template("level1_answer.html")


@app.route('/level2')
def level2():
    return render_template("level2.html")

@app.route('/level2_answer')
def level2_answer():
    return render_template("level2_answer.html")

@app.route('/level3')
def level3():
    return render_template("level3.html")

@app.route('/level3_answer')
def level3_answer():
    return render_template("level3_answer.html")


@app.route('/badge')
def badge():
    return render_template("badge.html")


levels_flow = {
    "level1": "level2",
    "level2": "level3",
    "level3": "graduation",
}


@app.route("/submit", methods=["POST"])
def submit():
    try:
        problem = request.json['problem']
        code = request.json['code']
        files = os.listdir("static/levels/" + problem)
        test_outputs = []
        result = {"error": "Timeout"}
        for i in range(len(files) / 2):
            try:
                input_file = "static/levels/%s/input%02d.txt" % (problem, i)
                output_file = "static/levels/%s/output%02d.txt" % (problem, i)
                expected = open(output_file).read()
                with capture_output() as c:
                    exec code
                actual = c.stdout
                test_output = expected == actual
                test_outputs.append(test_output)
            except Exception, e:
                test_outputs.append(False)
        test_outputs = all(test_outputs)
        if test_outputs:
            if levels_flow[problem] == "graduation":
                result = {
                    "graduation": "graduation"
                }
            else:
                result = {
                    "success": "success",
                    "next": levels_flow[problem]
                }
        else:
            result = {
                "error": "Wrong Answer"
            }
    except SyntaxError, e:
        result = {"error": "Syntax Error"}
    except Exception, e:
        traceback.print_exc()
        result = {
            "error": "Runtime Error",
            "message": str(e)
        }
    finally:
        return flask.jsonify(**result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
