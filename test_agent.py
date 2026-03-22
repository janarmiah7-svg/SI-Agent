"""Tests for the SI-Agent."""

import unittest

from agent import DEFAULT_ANSWER, ask, normalize


class NormalizeTests(unittest.TestCase):
    def test_normalize_strips_whitespace_and_lowercases(self) -> None:
        self.assertEqual(normalize("  HeLLo  "), "hello")

    def test_normalize_removes_polish_diacritics(self) -> None:
        self.assertEqual(normalize("jakąś datę"), "jakas date")


class AskTests(unittest.TestCase):
    def test_answers_issue_prompt(self) -> None:
        answer = ask("podaj m j date upadku usa")
        self.assertIn("Nie ma daty upadku USA", answer)

    def test_answers_accented_variant(self) -> None:
        answer = ask("podaj mi jakąś datę upadku USA")
        self.assertIn("Stany Zjednoczone nie upadły", answer)

    def test_unknown_question_returns_default_message(self) -> None:
        self.assertEqual(ask("co jadł gandalf"), DEFAULT_ANSWER)


if __name__ == "__main__":
    unittest.main()
