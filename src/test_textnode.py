import unittest

from textnode import TextNode, TextType, BlockType
from nodeconvert import text_node_to_html_node, block_to_block_type, get_leading_hashes, is_heading, is_code_block, is_quote, is_ordered_list, is_unordered_list

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.CODE_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is an image node", TextType.IMAGE, "http://localhost:8888/image.jpg")
        node2 = TextNode("This is an image node", TextType.IMAGE, "http://localhost:8888/image.jpg")
        self.assertEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("This is an image node", TextType.IMAGE, "http://localhost:8888/image.jpg")
        node2 = TextNode("This is an image node", TextType.IMAGE, "http://localhost:8888/image.png")
        self.assertNotEqual(node, node2)

    def test_nourl_neq(self):
        node = TextNode("This is an image node", TextType.IMAGE, "http://localhost:8888/image.jpg")
        node2 = TextNode("This is an image node", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_text_neq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a different text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code block", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code block")

    def test_image(self):
        node = TextNode("This is an alt text", TextType.IMAGE, "image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props["src"], "image.jpg")
        self.assertEqual(html_node.props["alt"], "This is an alt text")

    def test_image(self):
        node = TextNode("This is a link", TextType.LINK, "http://4chan.org/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props["href"], "http://4chan.org/")

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
        code_block = "```\nif code then whatever\nmore codecode\nend o code\n````"
        self.assertEqual(is_code_block(code_block), True)
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)
        code_block = "```\nif code then whatever\nmore codecode\nend o code\n```"
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

if __name__ == "__main__":
    unittest.main()
