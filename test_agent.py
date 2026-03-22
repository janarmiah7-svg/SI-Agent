"""Tests for the SI-Agent character search functionality."""

from agent import search


def test_search_by_name_gandalf():
    results = search("Gandalf")
    assert len(results) == 1
    assert results[0]["name"] == "Gandalf"


def test_search_by_alias_stary_zlodziej():
    results = search("stary złodziej")
    assert len(results) == 1
    assert results[0]["name"] == "Gandalf"
    assert results[0]["alias"] == "stary złodziej"


def test_search_case_insensitive():
    results = search("gandalf")
    assert len(results) == 1
    assert results[0]["name"] == "Gandalf"


def test_search_no_results():
    results = search("Sauron")
    assert results == []


def test_search_bilbo():
    results = search("Bilbo")
    assert len(results) == 1
    assert results[0]["name"] == "Bilbo Baggins"
