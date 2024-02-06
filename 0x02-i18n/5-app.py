#!/usr/bin/env python3
"""Mock logging in with a user."""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError
from typing import Union

app = Flask(__name__)
babel = Babel(app)


class Config:
    """Config for Babel timezone."""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_TIMEZONE = "UTC"
    BABEL_DEFAULT_LOCALE = "en"


app.config.from_object(Config)


def get_user(login_as: str) -> Union[str, None]:
    """Get user from mock db."""
    users = {"user": "User", "admin": "Admin"}
    return users.get(login_as, None)


@app.before_request
def before_request():
    """Set user before request."""
    g.user = get_user(request.args.get("login_as"))
    g.locale = get_locale()


def get_locale() -> Union[str, None]:
    """Get locale for user."""
    locale = request.args.get("locale")
    if locale and locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])
    # return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.localeselector
def get_locale_babel() -> str:
    """Get locale for babel."""
    if g.user:
        return g.locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/", methods=["GET"], strict_slashes=False)
def welcome() -> str:
    """Render template."""
    return render_template("5-index.html")
