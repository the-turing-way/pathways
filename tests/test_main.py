"""Tests for the main module."""

import unittest
from pathlib import Path
from unittest import mock

from pathways.main import (
    generate_landing_name,
    main,
    mask_parts,
)


class TestMain(unittest.TestCase):
    """Test main function from the main module."""

    def test_main(self):
        with mock.patch("sys.argv", ["pathways", "/path/to/my/book/"]):
            with mock.patch("pathways.main.pathways") as mock_build:
                main()
                mock_build.assert_called_once_with(Path("/path/to/my/book/"))

    def test_no_args(self):
        # self.assertRaises(SystemExit, main())
        with self.assertRaises(SystemExit) as exc:
            main()

        self.assertEqual(exc.exception.code, 2)


class TestMask(unittest.TestCase):
    """Test the mask_x functions from the main module."""

    maxDiff = None

    def test_chapters(self):
        parts = [{"file": "file1"}, {"file": "file2"}]
        allow_list = [
            "file1",
        ]

        expected = [{"file": "file1"}]
        actual = mask_parts(parts, allow_list)
        self.assertListEqual(expected, actual)

    def test_sections(self):
        parts = [
            {"file": "file1", "children": [{"file": "file2"}]},
            {"file": "file3", "children": [{"file": "file4"}]},
        ]
        allow_list = [
            "file1",
            "file2",
        ]

        expected = [{"file": "file1", "children": [{"file": "file2"}]}]
        actual = mask_parts(parts, allow_list)
        self.assertListEqual(expected, actual)

    def test_sub_sections(self):
        parts = [
            {
                "file": "file1",
                "children": [
                    {
                        "file": "file2",
                        "children": [{"file": "file3"}, {"file": "file4"}],
                    }
                ],
            },
        ]
        allow_list = [
            "file1",
            "file2",
            "file4",
        ]

        expected = [
            {
                "file": "file1",
                "children": [{"file": "file2", "children": [{"file": "file4"}]}],
            },
        ]
        actual = mask_parts(parts, allow_list)
        self.assertListEqual(expected, actual)

    def test_preserves_title(self):
        parts = [
            {
                "file": "file1",
                "title": "title1",
                "children": [
                    {
                        "file": "file2",
                        "title": "title2",
                        "children": [
                            {"title": "title3", "file": "file3"},
                            {"title": "title4", "file": "file4"},
                        ],
                    }
                ],
            },
        ]
        allow_list = [
            "file1",
            "file2",
            "file3",
        ]

        expected = [
            {
                "file": "file1",
                "title": "title1",
                "children": [
                    {
                        "title": "title2",
                        "file": "file2",
                        "children": [{"title": "title3", "file": "file3"}],
                    }
                ],
            },
        ]
        actual = mask_parts(parts, allow_list)
        self.assertListEqual(expected, actual)


class TestPathways(unittest.TestCase):
    """Test the pathways function from the main module."""

    def test_pathways(self):
        # ToDo Test main.pathways()
        pass


class TestGenerateLandingPageName(unittest.TestCase):
    def test_lowercase(self):
        expected = "dsg"
        actual = generate_landing_name("Dsg")
        self.assertEqual(expected, actual)

    def test_spaces(self):
        expected = "enrichment-students"
        actual = generate_landing_name("Enrichment Students")
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
