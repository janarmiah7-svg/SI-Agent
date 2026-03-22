"""Tests for the SI-Agent."""

import pytest

from agent import ask, normalize


class TestNormalize:
    def test_strips_whitespace(self):
        assert normalize("  hello  ") == "hello"

    def test_lower_cases(self):
        assert normalize("Hello World") == "hello world"

    def test_empty_string(self):
        assert normalize("") == ""


class TestAsk:
    def test_polish_gandalf_question(self):
        answer = ask("czemu gandalf ma brode")
        assert "Maiar" in answer
        assert "Istari" in answer

    def test_polish_gandalf_question_case_insensitive(self):
        answer = ask("Czemu Gandalf Ma Brode")
        assert len(answer) > 0
        assert "Maiar" in answer

    def test_english_gandalf_question(self):
        answer = ask("why does gandalf have a beard")
        assert "a Maia" in answer
        assert "Istari" in answer

    def test_unknown_question_returns_default(self):
        answer = ask("what is the capital of france")
        assert "Przepraszam" in answer or "Sorry" in answer

    def test_whitespace_is_ignored(self):
        answer = ask("  czemu gandalf ma brode  ")
        assert "Maiar" in answer
