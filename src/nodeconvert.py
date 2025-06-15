from textnode import TextType, BlockType
from leafnode import LeafNode
from parentnode import ParentNode
from markdown import text_to_textnodes, markdown_to_blocks

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

def text_nodes_to_html_nodes(text_nodes):
    rc = []
    for text_node in text_nodes:
        rc.append(text_node_to_html_node(text_node))
    return rc

def text_lines_to_html_nodes(lines):
    nodes = []
    for line in lines:
        nodes.extend(text_to_textnodes(line))
    return text_nodes_to_html_nodes(nodes)

def get_leading_hashes(lines):
    count = -1
    for line in lines:
        current_count = 0
        while line.startswith("#", current_count):
            current_count += 1
        if current_count == 0 or current_count > 6:
            return 0
        if not line.startswith(" ", current_count):
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
    stripped = block.strip("\n")
    #print(stripped[:3])
    #print(stripped.startswith("```") and stripped.startswith("```", len(stripped)-3))
    return stripped.startswith("```") and stripped.startswith("```", len(stripped)-3)

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
        return BlockType.QUOTE
    elif is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def header_to_html_nodes(header_block):
    lines = header_block.splitlines()
    header_num = get_leading_hashes(lines)
    if header_num == 0 or header_num > 6:
        raise ValueError("invalid header block passed to header_to_html_nodes()")
    stripped = list(map(lambda x: x[header_num+1:], header_block))
    leaves = text_lines_to_html_nodes(stripped)
    return ParentNode(f"h{header_num}", leaves)

def code_block_to_html_nodes(code_block):
    start = code_block.find("```\n") + 4
    end = code_block.rfind("```")
    stripped = code_block[start:end]
    #print(stripped)
    return ParentNode("pre", [LeafNode("code", stripped)])

def quote_block_to_html_nodes(quote_block):
    lines = quote_block.splitlines()
    stripped = list(map(lambda x: x[1:], lines))
    leaves = text_lines_to_html_nodes(stripped)
    return ParentNode("blockquote", leaves)

def unordered_list_to_html_nodes(unordered_list):
    lines = unordered_list.splitlines()
    stripped = list(map(lambda x: x[2:], lines))
    elements = []
    for line in stripped:
        nodes = text_lines_to_html_nodes([line])
        elements.append(ParentNode("li", nodes))
    return ParentNode("ul", elements)

def ordered_list_to_html_nodes(ordered_list):
    lines = ordered_list.splitlines()
    stripped = list(map(lambda x: x.split("- ", 1)[0], lines))
    elements = []
    for line in stripped:
        nodes = text_lines_to_html_nodes([line])
        elements.append(ParentNode("li", nodes))
    return ParentNode("ol", elements)

def paragraph_to_html_nodes(paragraph):
    merged = paragraph.replace("\n", " ")
    return ParentNode("p", text_lines_to_html_nodes([merged]))

block_map = {BlockType.HEADING:        header_to_html_nodes,
             BlockType.CODE:           code_block_to_html_nodes,
             BlockType.QUOTE:          quote_block_to_html_nodes,
             BlockType.UNORDERED_LIST: unordered_list_to_html_nodes,
             BlockType.ORDERED_LIST:   ordered_list_to_html_nodes,
             BlockType.PARAGRAPH:      paragraph_to_html_nodes}

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    #if block_to_block_type(blocks[0]) == BlockType.PARAGRAPH:
    #    print(blocks)
    leaves = []
    for block in blocks:
        #print(block_to_block_type(block))
        leaves.append(block_map[block_to_block_type(block)](block))
    return ParentNode("div", leaves)
