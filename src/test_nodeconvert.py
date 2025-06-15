import unittest

from textnode import BlockType
from nodeconvert import block_to_block_type, get_leading_hashes, is_heading, is_code_block, is_quote, is_ordered_list, is_unordered_list, markdown_to_html_node

class TestNodeConvert(unittest.TestCase):

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

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()
