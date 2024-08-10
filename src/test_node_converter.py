import unittest

from htmlnode import LeafNode
from textnode import TextNode
from node_converter import *

class Test_node_converter(unittest.TestCase):
    def test_invalid_text_type(self):
        node = TextNode("This is a text node", "BOLD")
        with self.assertRaises(Exception):
            self.assertEqual(text_node_to_html_node(node), "Not a valid text type.")
    
    def test_text_type_bold(self):
        node = TextNode("This is a text node", "bold")
        leafNode = LeafNode("b", "This is a text node")
        result = text_node_to_html_node(node)
        self.assertEqual(result.tag, leafNode.tag)
        self.assertEqual(result.value, leafNode.value)
        
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", Text_type.text.value)
        new_nodes = split_nodes_delimiter([node], "`", Text_type.code.value)
        expected = [
    TextNode("This is text with a ", Text_type.text.value),
    TextNode("code block", Text_type.code.value),
    TextNode(" word", Text_type.text.value),
]
        self.assertEqual(new_nodes, expected)
    
    def test_split_bold(self):
        node = TextNode("This is text with a **bold text** word", Text_type.text.value)
        new_nodes = split_nodes_delimiter([node], "**", Text_type.bold.value)
        expected = [
    TextNode("This is text with a ", Text_type.text.value),
    TextNode("bold text", Text_type.bold.value),
    TextNode(" word", Text_type.text.value),
]
        self.assertEqual(new_nodes, expected)
    
    def test_split_invalid(self):
        node = TextNode("This is text with a **bold text word", Text_type.text.value)
        with self.assertRaises(Exception):
            self.assertEqual(split_nodes_delimiter([node], "**", Text_type.bold.value), "That's invalid Markdown syntax.")

    def test_extract_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(expected, result)
    
    def test_extract_image_2(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(expected, result)
    
    def test_extract_links(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_links(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(expected, result)
    
    def test_extract_links_2(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_links(text)
        expected = [("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(expected, result)
        
    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            Text_type.text.value,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", Text_type.text.value),
            TextNode("to boot dev", Text_type.link.value, "https://www.boot.dev"),
            TextNode(" and ", Text_type.text.value),
            TextNode(
                "to youtube", Text_type.link.value, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(expected, new_nodes)
    
    def test_split_image(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            Text_type.text.value,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with a link ", Text_type.text.value),
            TextNode("to boot dev", Text_type.image.value, "https://www.boot.dev"),
            TextNode(" and ", Text_type.text.value),
            TextNode(
                "to youtube", Text_type.image.value, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(expected, new_nodes)
        
    def test_convert_text_to_text_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", Text_type.text.value), 
            TextNode("text", Text_type.bold.value), 
            TextNode(" with an ", Text_type.text.value), 
            TextNode("italic", Text_type.italic.value), 
            TextNode(" word and a ", Text_type.text.value), 
            TextNode("code block", Text_type.code.value, None), 
            TextNode(" and an ", Text_type.text.value), 
            TextNode("obi wan image", Text_type.image.value, "https://i.imgur.com/fJRm4Vk.jpeg"), 
            TextNode(" and a ", Text_type.text.value), 
            TextNode("link", Text_type.link.value, "https://boot.dev")
        ]
        self.assertEqual(expected, result)
        
    def test_markdown_to_html(self):
        markdown = '''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
'''
        result = markdown_to_html_node(markdown)
        expected = HTMLNode("html", 
                            children=[HTMLNode("h1", 
                                               children=[HTMLNode(None, "This is a heading", None, None)]), 
                                      HTMLNode("p", 
                                               children=[HTMLNode(None, "This is a paragraph of text. It has some "), 
                                                         HTMLNode("b", "bold"), 
                                                         HTMLNode(None, " and "), 
                                                         HTMLNode("i", "italic"), 
                                                         HTMLNode(None, " words inside of it.")]), 
                                      HTMLNode("ul", 
                                               children=[HTMLNode("li", 
                                                                  children=[HTMLNode(None, "This is the first list item in a list block")]), 
                                                         HTMLNode("li", 
                                                                  children=[HTMLNode(None, "This is a list item")]), 
                                                         HTMLNode("li", 
                                                                  children=[HTMLNode(None, "This is another list item")])])])
        
    def test_code_block_to_node(self):
        code_block = """```
func main(){
    fmt.Println("Hello, World!")
}
```"""
        result = code_block_to_node(code_block)
        expected = HTMLNode("pre", None, [HTMLNode("code", None, [HTMLNode(None, '''func main(){
    fmt.Println("Hello, World!")
}
''', None, None)], None)], None)
        self.assertEqual(result.tag, expected.tag)
        code_parent_result = result.children[0]
        code_parent_expected = expected.children[0]
        self.assertEqual(code_parent_result.children[0].value, code_parent_expected.children[0].value)
        