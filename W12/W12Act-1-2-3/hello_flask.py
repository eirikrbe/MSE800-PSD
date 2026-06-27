
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
    return f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{name} is learning Flask</title>
        </head>
        <body>
            <p>{name} is learning Flask with
               <a href='https://flask.palletsprojects.com/en/stable/quickstart/#'>Flask Documentation</a>
            </p>
        </body>
        <style>
            html {{
                background-color: #f0f0f0;
            }}  
            h1 {{
                color: #333;    }}
        </style>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)