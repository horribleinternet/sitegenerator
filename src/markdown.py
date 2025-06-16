from textnode import TextType, TextNode, BlockType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    delim_len = len(delimiter)
    if delim_len == 0:
        return old_nodes
    rc = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            rc.append(node)
            continue
        inside_block = False
        nodetext = node.text
        delim_pos = nodetext.find(delimiter)
        while delim_pos >= 0:
            if (delim_pos > 0):
                if inside_block:
                    rc.append(TextNode(nodetext[:delim_pos], text_type))
                else:
                    rc.append(TextNode(nodetext[:delim_pos], TextType.NORMAL_TEXT))
            inside_block = not inside_block
            nodetext = nodetext[delim_pos+delim_len:]
            delim_pos = nodetext.find(delimiter)
        if len(nodetext) > 0:
            if inside_block:
                raise Exception(f'unterminated block "{delimiter}"')
            else:
                rc.append(TextNode(nodetext, TextType.NORMAL_TEXT))
    return rc

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_complicated(old_nodes, splitter, img):
    rc = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            rc.append(node)
            continue
        comps = splitter(node.text)
        if len(comps) == 0:
            rc.append(node)
            continue
        marker = ""
        texttype = TextType.LINK
        if img:
            marker = "!"
            texttype = TextType.IMAGE
        remaining = node.text
        for comp in comps:
            pattern = f"{marker}[{comp[0]}]({comp[1]})"
            part = remaining.split(pattern, 1)
            if len(part[0]) > 0:
                rc.append(TextNode(part[0], TextType.NORMAL_TEXT))
            rc.append(TextNode(comp[0], texttype, comp[1]))
            remaining = remaining[len(part[0])+len(pattern):]
        if len(remaining) > 0:
            rc.append(TextNode(remaining, TextType.NORMAL_TEXT))
    return rc

def split_nodes_image(old_nodes):
    return split_nodes_complicated(old_nodes, extract_markdown_images, True)

def split_nodes_link(old_nodes):
    return split_nodes_complicated(old_nodes, extract_markdown_links, False)

def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text, TextType.NORMAL_TEXT)], "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        stripped_blocks.append(block.strip(" \n\t"))
    clean_blocks = []
    for block in stripped_blocks:
        if not block.isspace() and not block == "":
            clean_blocks.append(block)
    return clean_blocks

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

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        #print(line)
        if get_leading_hashes([line]) == 1:
            return line[2:]
    raise Exception("extract_title: markdown has no title")
