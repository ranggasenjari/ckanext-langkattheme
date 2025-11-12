from flask import Blueprint


langkattheme = Blueprint(
    "langkattheme", __name__)


def page():
    return "Hello, langkattheme!"


langkattheme.add_url_rule(
    "/langkattheme/page", view_func=page)


def get_blueprints():
    return [langkattheme]
