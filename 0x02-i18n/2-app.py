#!/usr/bin/env python3
""" Get locale from request """

from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)


class Config:
    """Config class"""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """
    Get locale from request.

    Returns:
        str: The best-matching language based on user preferences or default locale.
    """
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index():
    """
    Index page.

    Returns:
        str: Rendered HTML content.
    """
    return render_template("2-index.html")


if __name__ == "__main__":
    app.run()
