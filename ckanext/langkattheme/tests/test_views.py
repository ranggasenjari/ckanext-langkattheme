"""Tests for views.py."""

import pytest

import ckanext.langkattheme.validators as validators


import ckan.plugins.toolkit as tk


@pytest.mark.ckan_config("ckan.plugins", "langkattheme")
@pytest.mark.usefixtures("with_plugins")
def test_langkattheme_blueprint(app, reset_db):
    resp = app.get(tk.h.url_for("langkattheme.page"))
    assert resp.status_code == 200
    assert resp.body == "Hello, langkattheme!"
