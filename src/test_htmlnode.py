import unittest

from htmlnode import *

class Test_HTML_Node(unittest.TestCase):
    def test_props_to_html(self):
        test_props = {"href": "https://www.google.com", "target": "_blank",}
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        
    def test_repr(self):
        test_props = {"href": "https://www.google.com", "target": "_blank",}
        node2 = HTMLNode(props=test_props)
        self.assertEqual(node2.__repr__(), "HTMLNode(None, None, None, {'href': 'https://www.google.com', 'target': '_blank'})")
        
    def test_to_html(self):
        node3 = HTMLNode()
        try:
            node3.to_html()
        except NotImplementedError:
            result = True
        self.assertTrue(result)
    
    def test_leaf_node_to_html_para(self):
        paragraf = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(paragraf.to_html(), "<p>This is a paragraph of text.</p>")
    
    def test_leaf_node_to_html_url(self):
        url = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(url.to_html(), '<a href="https://www.google.com">Click me!</a>')
        
    def test_leaf_node_valueError(self):
        url = LeafNode("a", props={"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            self.assertEqual(url.to_html(), "All leaf nodes must have a value.")
    
    def test_parent_node_valueError(self):
        url = ParentNode("a", props={"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            self.assertEqual(url.to_html(), "All parent nodes must have a value for children.")
    
    def test_parent_node_valueError_2(self):
        url = ParentNode(children=[LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text"),], props={"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            self.assertEqual(url.to_html(), "All Parent nodes must have a value for tag.")
            
    def test_parent_node_to_html_no_props(self):
        node = ParentNode("p", children=[LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    
    def test_parent_node_to_html_nested_no_props(self):
        node = ParentNode("body", children=[ParentNode("title", children=[LeafNode(None, "TITLE")]),ParentNode("p", children=[LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")])])
        self.assertEqual(node.to_html(), "<body><title>TITLE</title><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></body>")
        