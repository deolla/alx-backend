#!/usr/bin/env python3
"""Uses user locales to determine the best supported language."""
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
    1: {"name": "Balou", "locale": "fr"},
    2: {"name": "Beyonce", "locale": "en"},
    3: {"name": "Spock", "locale": "kg"},
    4: {"name": "Teletubby", "locale": None},
}


def get_user(user_id: int) -> dict:
    """Get user from mock data."""
    return users.get(user_id)


@app.before_request
def before_request():
    """Before request."""
    user_id = request.args.get("login_as")
    if user_id:
        user = get_user(int(user_id))
        if user:
            from flask import g

            g.user = user


@babel.localeselector
def get_locale():
    """Get locale for user."""
    user = getattr(g, "user", None)
    if user:
        return user.get("locale")
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index():
    """Index page of the app."""
    return render_template("6-index.html")


if __name__ == "__main__":
    app.run()
