from re import *

def markdown_to_blocks(markdown):
    return [item.strip() for item in markdown.split("\n\n") if len(item) != 0]

def block_to_block_type(markdown_block):
    if fullmatch(r"#{1,6}\s.*", markdown_block):
        return "heading"
    elif fullmatch(r"`{3}\n?(.*\n?)+`{3}", markdown_block):
        return "code"
    elif fullmatch(r"(>\s.*\n?)+", markdown_block):
        return "quote"
    elif fullmatch(r"([*-]\s.*\n?)+", markdown_block):
        return "unordered list"
    elif fullmatch(r"(\d\.\s.*\n?)+", markdown_block):
        list_numbers = findall(r"(\d)\.\s.*\n?", markdown_block)
        result = True
        for i in range(len(list_numbers)):
            if i + 1 == int(list_numbers[i]):
                continue
            else:
                return "paragraph"
        if result:
            return "ordered list"
    else:
        return "paragraph"
    