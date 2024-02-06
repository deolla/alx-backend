#!/usr/bin/env python3
"""A Basic Flask app that returns a simple HTML page."""
from flask import Flask, render_template

app = Flask(__name__, template_folder="./templates")


@app.route("/")
def index():
    """Index page of the app that returns a simple HTML page."""
    return render_template("0-index.html")


if __name__ == "__main__":
    app.run(debug=True)
