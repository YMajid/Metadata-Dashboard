import flask
from flaskblog import app

# if __name__ == '__main__':
#     app.run(debug=True)

app = flask.Flask("__main__")

@app.route("/")
def my_index():
    return flask.render_template("index.html", token="Hello world")

app.run(debug=True)