#!/usr/bin/env python3
"""Task 100: Create a user locale and timezone support in a Flask app."""
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz
import locale
from datetime import datetime

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
def before_request() -> None:
    """_summary_"""
    user = get_user()
    g.user = user

    time_now = pytz.utc.localize(datetime.utcnow())
    time = time_now.astimezone(pytz.timezone(get_timezone()))
    locale.setlocale(locale.LC_TIME, (get_locale(), "UTF-8"))
    time_format = "%b %d, %Y %I:%M:%S %p"
    g.time = time.strftime(time_format)


@babel.localeselector
def get_locale():
    """_summary_

    Returns:
                                    _type_: _description_
    """
    # Locale from URL parameters
    locale = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        return locale

    # Locale from user settings
    if g.user:
        locale = g.user.get("locale")
        if locale and locale in app.config["LANGUAGES"]:
            return locale

    # ocale from request header
    locale = request.headers.get("locale", None)
    if locale in app.config["LANGUAGES"]:
        return locale

        # Default locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


# babel.init_app(app, locale_selector=get_locale)


@babel.timezoneselector
def get_timezone():
    """
    Select and return appropriate timezone
    """
    # Find timezone parameter in URL parameters
    tzone = request.args.get("timezone", None)
    if tzone:
        try:
            return pytz.timezone(tzone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Find time zone from user settings
    if g.user:
        try:
            tzone = g.user.get("timezone")
            return pytz.timezone(tzone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Default to UTC
    default_tz = app.config["BABEL_DEFAULT_TIMEZONE"]
    return default_tz


@app.route("/")
def index():
    """_summary_"""
    return render_template("5-index.html")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
