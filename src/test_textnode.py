import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test_eq_2(self):
        node3 = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node4 = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertEqual(node3, node4)
    
    def test_url_none(self):
        node5 = TextNode("This is a text node", "bold", None)
        node6 = TextNode("This is a text node", "bold", None)
        self.assertEqual(node5, node6)
    
    def test_ne(self):
        node7 = TextNode("This is a text node", "italic", None)
        node8 = TextNode("This is a text node", "bold", None)
        self.assertNotEqual(node7, node8)


if __name__ == "__main__":
    unittest.main()