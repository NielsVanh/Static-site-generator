import unittest

from main import extract_title

class Test_main(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# There is h1 header."
        result = extract_title(markdown)
        expected = "There is h1 header."
        self.assertEqual(result, expected)
    
    def test_extract_title_exception(self):
        markdown = "## There is h1 header."
        with self.assertRaises(Exception):
            self.assertEqual(extract_title(markdown), "There is no h1 header.")