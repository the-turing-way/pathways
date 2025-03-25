"""Tests for the cards module."""

import unittest

from pathways.card import create_card, create_panel, insert_text_after_string


class TestCreateCard(unittest.TestCase):
    """Tests for the create_card function."""

    def test_simple(self):
        file_list = [
            "welcome",
            "communication/communication",
            "communication/comms-overview",
            "communication/comms-overview/comms-overview-principles",
        ]
        actual = create_card("SomePersona", file_list, "sinner")
        expected = (
            ":::{card} SomePersona\n"
            ":link: pathways/sinner\n"
            "- [](./welcome)\n"
            "- [](./communication/communication)\n"
            "- [](./communication/comms-overview)\n"
            "\nAnd more…\n"
            "\n:::"
        )
        self.assertEqual(expected, actual)


class TestGeneratePanel(unittest.TestCase):
    """Tests for the create_panel function."""

    def test_simple(self):
        list_of_cards = ["one", "two"]
        actual = create_panel(list_of_cards)
        expected = "::::{grid} 1 1 2 2\none\ntwo\n::::\n"
        self.assertEqual(expected, actual)


class TestInsertTextAfterString(unittest.TestCase):
    """Tests for the insert_text_after_string function."""

    def test_simple(self):
        input_str = "## Different Pathways"
        panel_str = "::::{grid} 1 1 2 2\none\ntwo\n\n::::\n"
        expected = "## Different Pathways\n" + panel_str
        actual = insert_text_after_string(input_str, "## Different Pathways", panel_str)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
