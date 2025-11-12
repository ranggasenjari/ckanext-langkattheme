"""Tests for helpers.py."""

import ckanext.langkattheme.helpers as helpers


def test_langkattheme_hello():
    assert helpers.langkattheme_hello() == "Hello, langkattheme!"
