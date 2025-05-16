"""Tests for the landing-page class."""

import json
import unittest

from pathways.landing_page import LandingPage


class TestGetPageTitle(unittest.TestCase):
    """Tests for generate_badge function."""

    def test_simple(self):
        a_landing_page = LandingPage("test_persona", "test")
        curated_page_path = "tests/test_files/test_landing/welcome.md"
        actual = a_landing_page.get_title_from_curated_page(curated_page_path)
        expected = "Welcome"
        self.assertEqual(expected, actual)
        pass


class TestGetCuratedList(unittest.TestCase):
    """Tests for generate_badge function."""

    def test_simple(self):
        a_landing_page = LandingPage("test", "sinner")
        allow_listed_toc_path = "tests/test_files/test_landing/toc_allow_list.json"
        with open(allow_listed_toc_path) as f:
            toc = json.load(f)
        a_landing_page.gather_curated_links(toc)
        actual = a_landing_page.curated_links
        expected = [
            "[](../communication/communication)",
            [
                "[](../communication/comms-overview)",
                ["[](../communication/comms-overview/comms-overview-principles)"],
            ],
        ]
        self.assertEqual(actual, expected)
