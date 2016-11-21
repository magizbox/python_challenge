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

@app.route('/level2')
def level2():
    return render_template("level2.html")


@app.route('/badge')
def badge():
    return render_template("badge.html")

levels_flow = {
    "level1": "level2",
    "level2": "graduation"
}
@app.route("/submit", methods=["POST"])
def execute():
    try:
        problem = request.json['problem']
        code = request.json['code']
        files = os.listdir("static/levels/" + problem)
        results = []
        for i in range(len(files) / 2):
            input_file = "static/levels/%s/input%02d.txt" % (problem, i)
            output_file = "static/levels/%s/output%02d.txt" % (problem, i)
            expected = open(output_file).read()
            with capture_output() as c:
                exec code
            actual = c.stdout
            result = expected == actual
            results.append(result)
        results = all(results)
        if results:
            if levels_flow[problem] == "graduation":
                result = {
                    "graduation": "graduation"
                }
            else:
                result = {
                    "success": "success",
                    "next": "level2"
                }
        else:
            result = {
                "error": "Wrong Answer"
            }
    except SyntaxError, e:
        result = {"error": "Syntax Error"}
    except Exception, e:
        result = {"error": str(e)}
    finally:
        return flask.jsonify(**result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
