#!/usr/bin/env python3
"""Creating a user login system is outside
the scope of this project."""

from flask import Flask, render_template, request, g
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
    locale = request.args.get("locale")
    if locale and locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id: int) -> dict:
    """
    Get user information based on user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary containing user information.
    """
    return users.get(user_id) if user_id else None


@app.before_request
def before_request():
    """
    Execute before all other functions.
    Set the user information in the Flask global object (g).
    """
    user_id = int(request.args.get("login_as", 0))
    g.user = get_user(user_id)


@app.route("/")
def index() -> str:
    """
    Render the index template.

    Returns:
        str: Rendered HTML content.
    """
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run()
