"""Tests for the SI-Agent entity merge demo."""

import unittest

from agent import SOURCE_RECORDS, describe_entity, find_entity, merge_records, normalize


class NormalizeTests(unittest.TestCase):
    def test_normalize_removes_accents(self):
        self.assertEqual(normalize(" Stary Złodziej "), "stary zlodziej")


class MergeRecordsTests(unittest.TestCase):
    def test_merge_records_combines_matching_sources(self):
        merged = merge_records(SOURCE_RECORDS)

        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["canonical_name"], "Gandalf")
        self.assertEqual(
            merged[0]["sources"],
            ["CEIDG", "KRS", "network_localization"],
        )
        self.assertIn("stary złodziej", merged[0]["aliases"])


class FindEntityTests(unittest.TestCase):
    def test_find_entity_resolves_alias_to_canonical_name(self):
        entity = find_entity("stary zlodziej")

        self.assertIsNotNone(entity)
        self.assertEqual(entity["canonical_name"], "Gandalf")


class DescribeEntityTests(unittest.TestCase):
    def test_describe_entity_lists_combined_sources(self):
        description = describe_entity("Mithrandir")

        self.assertIn("Gandalf", description)
        self.assertIn("CEIDG", description)
        self.assertIn("KRS", description)

    def test_unknown_entity_returns_default_message(self):
        self.assertEqual(
            describe_entity("Saruman"),
            "Nie znaleziono powiązanego bytu.",
        )


if __name__ == "__main__":
    unittest.main()
