from textnode import TextType, TextNode
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
