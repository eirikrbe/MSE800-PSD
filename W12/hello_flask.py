
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello_flask():
    return "<p>Hello, Flask!</p>"


@app.route("/bye")
def say_bye():
    return "<p>Goodbye, Flask!</p>"

@app.route("/username/<name>")
def learn(name):
    return f"<p>{name} is learning Flask!</p>"

if __name__ == "__main__":
    app.run(debug=True)