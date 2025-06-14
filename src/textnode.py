from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    HEADING = "headng"
    CODE = "oode blockc"
    QUOTE = "quote"
    UNORDERED_LIST = "uordered list"
    ORDERED_lIST = "ordered list"
    PARAGRAPH = "paragraph"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL_TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src":text_node.url, "alt":text_node.text})
        case _:
            raise ValueError("invalide TextType")

def get_leading_hashes(lines):
    count = -1
    for line in lines:
        current_count = 0
        #print()
        #print(line)
        while line.startswith("#", current_count):
            current_count += 1
        #print(current_count)
        #print(line)
        #print(line[current_count:])
        if current_count == 0 or current_count > 6:
            return 0
        if not line.startswith(" ", current_count):
            #print(line.startswith(" ", current_count))
            return 0
        if count != -1 and count != current_count:
            return 0
        else:
            count = current_count
    return count

def is_heading(block):
    lines = block.splitlines()
    return get_leading_hashes(lines) > 0

def is_code_block(block):
    return block.startswith("~~~") and block.startswith("~~~", len(block)-4)

def block_startswith(block, start):
    lines = block.splitlines()
    for line in lines:
        if not line.startswith(start):
            return False
    return True

def is_quote(block):
    return block_startswith(block, ">")

def is_unordered_list(block):
    return block_startswith(block, "- ")

def is_ordered_list(block):
    lineno = 1
    lines = block.splitlines()
    for line in lines:
        if not line.startswith(f"{lineno}- "):
            return False
        lineno += 1
    return True

def block_to_block_type(block):
    if is_heading(block):
        return BlockType.HEADING
    elif is_code_block(block):
        return BlockType.CODE
    elif is_quote(block):
        return BlockType.CODE
    elif is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_lIST
    else:
        return BlockType.PARAGRAPH
