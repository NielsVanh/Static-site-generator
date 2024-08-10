import unittest

from block_converter import *

class Test_block_converter(unittest.TestCase):
    def test_markdown_to_blocks(self):
        document = "   # This is a heading    \n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"
        result = markdown_to_blocks(document)
        expected = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        self.assertEqual(expected, result)
    
    def test_markdown_to_blocks_2(self):
        document = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"
        result = markdown_to_blocks(document)
        expected = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        self.assertEqual(expected, result)
        
    def test_block_to_block_type_heading(self):
        markdown_block = "### hjghj"
        result = block_to_block_type(markdown_block)
        expected = "heading"
        self.assertEqual(expected, result)
    
    def test_block_to_block_type_code(self):
        markdown_block = "```hjghj```"
        result = block_to_block_type(markdown_block)
        expected = "code"
        self.assertEqual(expected, result)
    
    def test_block_to_block_type_quote(self):
        markdown_block = ">hjghj\n>ghf"
        result = block_to_block_type(markdown_block)
        expected = "quote"
        self.assertEqual(expected, result)
    
    def test_block_to_block_type_unordered_list(self):
        markdown_block = "* hjghj\n* ghf"
        result = block_to_block_type(markdown_block)
        expected = "unordered list"
        self.assertEqual(expected, result)
    
    def test_block_to_block_type_ordered_list(self):
        markdown_block = "1. hjghj\n2. ghf"
        result = block_to_block_type(markdown_block)
        expected = "ordered list"
        self.assertEqual(expected, result)
    
    def test_block_to_block_type_not_ordered_list(self):
        markdown_block = "1. hjghj\n3. ghf"
        result = block_to_block_type(markdown_block)
        expected = "paragraph"
        self.assertEqual(expected, result)
    
    def test_block_to_block_type_paragraph(self):
        markdown_block = " hjghj ghf"
        result = block_to_block_type(markdown_block)
        expected = "paragraph"
        self.assertEqual(expected, result)