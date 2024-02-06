#!/usr/bin/env python3
"""A Mock logging in a"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz

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


@babel.localeselector
def get_locale() -> str:
    """
    Get locale from request and return locale.
    """
    opts = [
        request.args.get("locale", "").strip(),
        g.user.get("locale", None) if g.user else None,
        request.accept_languages.best_match(app.config["LANGUAGES"]),
        Config.BABEL_DEFAULT_LOCALE,
    ]
    for locale in opts:
        if locale and locale in Config.LANGUAGES:
            return locale


@babel.timezoneselector
def get_timezone() -> str:
    """
    Get timezone from request and return timezone.
    """
    timee = request.args.get("timezone", "").strip()
    if not timee and g.user:
        timee = g.user["timezone"]
    try:
        return pytz.timezone(timee).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config["BABEL_DEFAULT_TIMEZONE"]


@app.before_request
def before_request():
    """Before each request."""
    user_id = int(request.args.get("login_as", 0))
    g.user = get_user(user_id) if user_id else None


@app.route("/")
def index():
    """Index page of the app."""
    return render_template("6-index.html")


if __name__ == "__main__":
    app.run()
