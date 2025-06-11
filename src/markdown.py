from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    delim_len = len(delimiter)
    if delim_len == 0:
        return old_nodes
    rc = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
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

