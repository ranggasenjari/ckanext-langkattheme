"""Tests for validators.py."""

import pytest

import ckan.plugins.toolkit as tk

from ckanext.langkattheme.logic import validators


def test_langkattheme_reauired_with_valid_value():
    assert validators.langkattheme_required("value") == "value"


def test_langkattheme_reauired_with_invalid_value():
    with pytest.raises(tk.Invalid):
        validators.langkattheme_required(None)
