#!/usr/bin/env python3
"""A Mock logging in and out of a user."""
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

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id: int) -> dict:
    """Get user from mock data."""
    return users.get(user_id)


@app.before_request
def before_request():
    """Before request, get user from mock data."""
    user_id = request.args.get("login_as", 0)
    g.user = get_user(user_id) if user_id else None


@app.route("/")
def index():
    """Index page of the app."""
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run()
