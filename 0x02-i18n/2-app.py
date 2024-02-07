#!/usr/bin/env python3
"""Create a get_locale function with
the babel.localeselector decorator.
"""
from flask import Flask, render_template, request
from flask_babel import Babel

# configure the flask app
app = Flask(__name__)
babel = Babel(app)


class Config(object):
    """
    Create a Config object

    Args:
        object (object): object

    Returns:
        object: object
    """

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """
    get locale from request

    Returns:
        str: best match language
    """
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index():
    """
    Render a template

    Returns:
        str: render template
    """
    return render_template("2-index.html")


if __name__ == "__main__":
    app.run()
