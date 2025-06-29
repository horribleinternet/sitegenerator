import unittest

from textnode import TextType, TextNode, BlockType
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, get_leading_hashes, is_heading, is_code_block, is_quote, is_ordered_list, is_unordered_list, extract_title

class TestParentNode(unittest.TestCase):

    def test_bold_mid(self):
        old_nodes = [TextNode("this has **bold** text", TextType.NORMAL_TEXT)]
        nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD_TEXT)
        self.assertEqual(nodes, [TextNode("this has ", TextType.NORMAL_TEXT),
                                 TextNode("bold", TextType.BOLD_TEXT),
                                 TextNode(" text", TextType.NORMAL_TEXT)])

    def test_bold_start(self):
        old_nodes = [TextNode("**bold** text this has", TextType.NORMAL_TEXT)]
        nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD_TEXT)
        self.assertEqual(nodes, [TextNode("bold", TextType.BOLD_TEXT),
                                 TextNode(" text this has", TextType.NORMAL_TEXT)])

    def test_bold_end(self):
        old_nodes = [TextNode("this has text that is **bold**", TextType.NORMAL_TEXT)]
        nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD_TEXT)
        self.assertEqual(nodes, [TextNode("this has text that is ", TextType.NORMAL_TEXT),
                                 TextNode("bold", TextType.BOLD_TEXT)])

    def test_bold_two(self):
        old_nodes = [TextNode("this has **bold** text and **other bold** text", TextType.NORMAL_TEXT)]
        nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD_TEXT)
        self.assertEqual(nodes, [TextNode("this has ", TextType.NORMAL_TEXT),
                                 TextNode("bold", TextType.BOLD_TEXT),
                                 TextNode(" text and ", TextType.NORMAL_TEXT),
                                 TextNode("other bold", TextType.BOLD_TEXT),
                                 TextNode(" text", TextType.NORMAL_TEXT)])

    def test_code(self):
        old_nodes = [TextNode("there is some `code` here", TextType.NORMAL_TEXT)]
        nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE_TEXT)
        self.assertEqual(nodes, [TextNode("there is some ", TextType.NORMAL_TEXT),
                                 TextNode("code", TextType.CODE_TEXT),
                                 TextNode(" here", TextType.NORMAL_TEXT)])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) really")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        matches = extract_markdown_images("![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        matches = extract_markdown_images("an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        matches = extract_markdown_images("![image](https://i.imgur.com/zjjcJKZ.png) is")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://www.boot.dev)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links("[image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        matches = extract_markdown_links("![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([], matches)
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
        matches = extract_markdown_links("This is text with a [link](https://www.boot.dev) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes
        )
        anothernode = TextNode("This is other text with an ![horrible](https://goatse.cx/giver.jpg) and an other ![terrible](https://goatse.cx/ring.jpg)",
            TextType.NORMAL_TEXT
        )
        new_nodes = split_nodes_image([node, anothernode])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is other text with an ", TextType.NORMAL_TEXT),
                TextNode("horrible", TextType.IMAGE, "https://goatse.cx/giver.jpg"),
                TextNode(" and an other ", TextType.NORMAL_TEXT),
                TextNode("terrible", TextType.IMAGE, "https://goatse.cx/ring.jpg"),
            ],
            new_nodes
        )
        morenode = TextNode("![horrible](https://goatse.cx/giver.jpg)![](https://goatse.cx/ring.jpg)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([morenode])
        self.assertListEqual(
            [
                TextNode("horrible", TextType.IMAGE, "https://goatse.cx/giver.jpg"),
                TextNode("", TextType.IMAGE, "https://goatse.cx/ring.jpg"),
            ],
            new_nodes
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.htm) and another [second link](https://i.imgur.com/3elNhQu.htm)",
            TextType.NORMAL_TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.htm"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.htm"),
            ],
            new_nodes
        )
        anothernode = TextNode("This is other text with an [horrible](https://goatse.cx/giver.htm) and an other [terrible](https://goatse.cx/ring.htm)",
            TextType.NORMAL_TEXT
        )
        new_nodes = split_nodes_link([node, anothernode])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.htm"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.htm"),
                TextNode("This is other text with an ", TextType.NORMAL_TEXT),
                TextNode("horrible", TextType.LINK, "https://goatse.cx/giver.htm"),
                TextNode(" and an other ", TextType.NORMAL_TEXT),
                TextNode("terrible", TextType.LINK, "https://goatse.cx/ring.htm"),
            ],
            new_nodes
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL_TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with an ", TextType.NORMAL_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word and a ", TextType.NORMAL_TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" and an ", TextType.NORMAL_TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL_TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        new_nodes
        )

        text2 = "This is **text** with ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) an _italic_ word [link](https://boot.dev) and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes2 = text_to_textnodes(text2)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL_TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with ", TextType.NORMAL_TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" an ", TextType.NORMAL_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word ", TextType.NORMAL_TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and a ", TextType.NORMAL_TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" and an ", TextType.NORMAL_TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL_TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        new_nodes2
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items





This is **bolded** paragraph

       



   This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            ],
        )

    def test_heading(self):
        heading = "## what\n## why\n"
        self.assertEqual(get_leading_hashes(heading.splitlines()), 2)
        self.assertEqual(is_heading(heading), True)
        self.assertEqual(block_to_block_type(heading), BlockType.HEADING)
        heading = "## what\n### why\n## where"
        self.assertEqual(get_leading_hashes(heading.splitlines()), 0)
        self.assertEqual(is_heading(heading), False)
        self.assertEqual(block_to_block_type(heading), BlockType.PARAGRAPH)
        heading = "##what\n## why\n"
        self.assertEqual(get_leading_hashes(heading.splitlines()), 0)
        self.assertEqual(is_heading(heading), False)
        self.assertEqual(block_to_block_type(heading), BlockType.PARAGRAPH)
        heading = "#### what\n#### why\n#### where\n#### how\n"
        self.assertEqual(get_leading_hashes(heading.splitlines()), 4)
        self.assertEqual(is_heading(heading), True)
        self.assertEqual(block_to_block_type(heading), BlockType.HEADING)

    def test_code_block(self):
        code_block = "\n```\nif code then whatever\nmore codecode\nend o code\n```\n"
        self.assertEqual(is_code_block(code_block), True)
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)
        code_block = "\n``\nif code then whatever\nmore codecode\nend o code\n``\n"
        self.assertEqual(is_code_block(code_block), False)
        self.assertEqual(block_to_block_type(code_block), BlockType.PARAGRAPH)

    def test_quote(self):
        quote_block=">racist stuff\n>misogynistic stuf\n>retarded stuff\n"
        self.assertEqual(is_quote(quote_block), True)
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)
        quote_block=">racist stuff\nmisogynistic stuf\n>retarded stuff\n"
        self.assertEqual(is_quote(quote_block), False)
        self.assertEqual(block_to_block_type(quote_block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        unordered_list = "- some BS\n- some other BS\n- even more BS\n"
        self.assertEqual(is_unordered_list(unordered_list), True)
        self.assertEqual(block_to_block_type(unordered_list), BlockType.UNORDERED_LIST)
        unordered_list = "-some BS\n- some other BS\n- even more BS\n"
        self.assertEqual(is_unordered_list(unordered_list), False)
        self.assertEqual(block_to_block_type(unordered_list), BlockType.PARAGRAPH)
        unordered_list = "some BS\nsome other BS\neven more BS\n"
        self.assertEqual(is_unordered_list(unordered_list), False)
        self.assertEqual(block_to_block_type(unordered_list), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        ordered_list = "1- some BS\n2- some other BS\n3- even more BS\n"
        self.assertEqual(is_ordered_list(ordered_list), True)
        self.assertEqual(block_to_block_type(ordered_list), BlockType.ORDERED_LIST)
        ordered_list = "2-some BS\n1- some other BS\n3- even more BS\n"
        self.assertEqual(is_ordered_list(ordered_list), False)
        self.assertEqual(block_to_block_type(ordered_list), BlockType.PARAGRAPH)
        ordered_list = "some BS\nsome other BS\neven more BS\n"
        self.assertEqual(is_ordered_list(ordered_list), False)
        self.assertEqual(block_to_block_type(ordered_list), BlockType.PARAGRAPH)

    def test_paragraph(self):
        paragraph = "oh noes\nteh bus\n"
        self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)
        code_block = "```\nif code then whatever\nmore codecode\nend o code\n````"
        self.assertNotEqual(block_to_block_type(code_block), BlockType.PARAGRAPH)
        heading = "#### what\n#### why\n"
        self.assertNotEqual(block_to_block_type(heading), BlockType.PARAGRAPH)

    def test(self):
        md = """

# Title Title Titled

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
"""
        title = extract_title(md)
        self.assertEqual(title, "Title Title Titled")