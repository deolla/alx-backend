#!/usr/bin/env python3
"""Parametrize templates for language and date."""
from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)


class Config(object):
    """Config class for the app in Flask."""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Get the locale from the request"""
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index():
    """Index page of the app."""
    return render_template("3-index.html")


if __name__ == "__main__":
    app.run()
