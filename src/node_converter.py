from textnode import *
from htmlnode import *
from block_converter import *

from enum import Enum
from re import *

class Text_type(Enum):
    text = "text"
    bold = "bold"
    italic = "italic"
    code = "code"
    link = "link"
    image = "image"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case Text_type.text.value:
            return LeafNode(None, text_node.text)
        case Text_type.bold.value:
            return LeafNode("b", text_node.text)
        case Text_type.italic.value:
            return LeafNode("i", text_node.text)
        case Text_type.code.value:
            return LeafNode("code", text_node.text)
        case Text_type.link.value:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case Text_type.image.value:
            return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
        
        case _:
            raise Exception("Not a valid text type.")
        

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    text_nodes = []
    for old_node in old_nodes:
        texts = old_node.text.split(delimiter)
        if len(texts) % 2 == 0:
            raise Exception("That's invalid Markdown syntax.")
        else:
            for i in range(len(texts)):
                if len(texts[i]) == 0:
                    continue
                elif i % 2 == 0:
                    text_nodes.append(TextNode(texts[i], old_node.text_type))
                else:
                    text_nodes.append(TextNode(texts[i], text_type))
    return text_nodes

def extract_markdown_images(text):
    return findall(r"\!\[(.*?)\]\((.+?)\)", text)

def extract_markdown_links(text):
    return findall(r"(?<!!)\[(.*?)\]\((.+?)\)", text)

def split_nodes_image(old_nodes):
    text_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        texts = []
        if len(images) == 0:
            text_nodes.append(old_node)
        else:
            for image in images:
                image_text = image[0]
                image_url = image[1]
                if len(images) == 1:
                    texts.extend(old_node.text.split(f"![{image_text}]({image_url})"))
                    texts.insert(1, image)
                else:
                    if len(texts) == 0:
                        texts.extend(old_node.text.split(f"![{image_text}]({image_url})"))
                        texts.insert(1, image)
                    else:
                        last_text = texts[-1]
                        texts.pop()
                        texts.extend(last_text.split(f"![{image_text}]({image_url})"))
                        texts.insert(-1, image)
            for i in range(len(texts)):
                if len(texts[i]) == 0:
                    continue
                elif i % 2 == 0:
                    text_nodes.append(TextNode(texts[i], old_node.text_type))
                else:
                    alt_text = texts[i][0]
                    url = texts[i][1]
                    text_nodes.append(TextNode(alt_text, Text_type.image.value, url))
    return text_nodes

def split_nodes_link(old_nodes):
    text_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        texts = []
        if len(links) == 0:
            text_nodes.append(old_node)
        else:
            for link in links:
                link_text = link[0]
                link_url = link[1]
                if len(links) == 1:
                    texts.extend(old_node.text.split(f"[{link_text}]({link_url})"))
                    texts.insert(1, link)
                else:
                    if len(texts) == 0:
                        texts.extend(old_node.text.split(f"[{link_text}]({link_url})"))
                        texts.insert(1, link)
                    else:
                        last_text = texts[-1]
                        texts.pop()
                        texts.extend(last_text.split(f"[{link_text}]({link_url})"))
                        texts.insert(-1, link)
            for i in range(len(texts)):
                    if len(texts[i]) == 0:
                        continue
                    elif i % 2 == 0:
                        text_nodes.append(TextNode(texts[i], old_node.text_type))
                    else:
                        alt_text = texts[i][0]
                        url = texts[i][1]
                        text_nodes.append(TextNode(alt_text, Text_type.link.value, url))
    return text_nodes

def text_to_textnodes(text):
    text_nodes = split_nodes_delimiter([TextNode(text, Text_type.text.value)], "**", Text_type.bold.value)
    text_nodes = split_nodes_delimiter(text_nodes, "*", Text_type.italic.value)
    text_nodes = split_nodes_delimiter(text_nodes, "`", Text_type.code.value)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes

def heading_block_to_node(block):
    block_items = findall(r"(#{1,6})\s(.*)", block)
    item = block_items[0]
    item_tag = item[0]
    parent_tag = f"h{len(item_tag)}"
    item_text = item[1]
    leafnodes = []
    text_nodes = text_to_textnodes(item_text)
    for textnode in text_nodes:
        leafnodes.append(text_node_to_html_node(textnode))
    return ParentNode(parent_tag, children=leafnodes)

def code_block_to_node(block):
    block_items = findall(r"`{3}\n?((.*\n?)+)`{3}", block)
    tuple = block_items[0]
    item = tuple[0]
    block_tag = "code"
    parent_tag = "pre"
    item_text = item
    leafnodes = []
    text_nodes = text_to_textnodes(item_text)
    for textnode in text_nodes:
        leafnodes.append(text_node_to_html_node(textnode))
    block_node = [ParentNode(block_tag, children=leafnodes)]
    return ParentNode(parent_tag, children=block_node)


def quote_block_to_node(block):
    block_items = findall(r">\s(.*)\n?", block)
    parent_tag = "blockquote"
    leafnodes = []
    for item in block_items:
        item_text = item
        text_nodes = text_to_textnodes(item_text)
        for textnode in text_nodes:
            leafnodes.append(text_node_to_html_node(textnode))
    return ParentNode(parent_tag, children=leafnodes)

def unordered_list_block_to_node(block):
    block_items = findall(r"[*-]\s(.*)\n?", block)
    block_tag = "li"
    parent_tag = "ul"
    list_nodes = []
    for item in block_items:
        item_text = item
        text_nodes = text_to_textnodes(item_text)
        for textnode in text_nodes:
            leafnodes = []
            leafnodes.append(text_node_to_html_node(textnode))
            list_nodes.append(ParentNode(block_tag, children=leafnodes))
    return ParentNode(parent_tag, children=list_nodes)

def ordered_list_block_to_node(block):
    block_items = findall(r"\d\.\s(.*)\n?", block)
    block_tag = "li"
    parent_tag = "ol"
    list_nodes = []
    for item in block_items:
        item_text = item
        text_nodes = text_to_textnodes(item_text)
        for textnode in text_nodes:
            leafnodes = []
            leafnodes.append(text_node_to_html_node(textnode))
            list_nodes.append(ParentNode(block_tag, children=leafnodes))
    return ParentNode(parent_tag, children=list_nodes)

def paragraph_block_to_node(block):
    parent_tag = "p"
    text_nodes = text_to_textnodes(block)
    leafnodes = []
    for textnode in text_nodes:
        leafnodes.append(text_node_to_html_node(textnode))
    return ParentNode(parent_tag, children=leafnodes)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    tag = "html"
    children = []
    for block in blocks:
        if block_to_block_type(block) == "heading":
            children.append(heading_block_to_node(block))
        elif block_to_block_type(block) == "code":
            children.append(code_block_to_node(block))
        elif block_to_block_type(block) == "quote":
            children.append(quote_block_to_node(block))
        elif block_to_block_type(block) == "unordered list":
            children.append(unordered_list_block_to_node(block))
        elif block_to_block_type(block) == "ordered list":
            children.append(ordered_list_block_to_node(block))
        else:
            children.append(paragraph_block_to_node(block))
    return ParentNode(tag, children=children)
