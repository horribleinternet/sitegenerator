import unittest

from nodeconvert import markdown_to_html_node

class TestNodeConvert(unittest.TestCase):

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

    def test_header(self):
        md = """
# This is text that _should_ remain

## the **same** even with inline stuff

### This is text that _should_ remain

#### the **same** even with inline stuff

##### This is text that _should_ remain

###### the **same** even with inline stuff

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is text that <i>should</i> remain</h1><h2>the <b>same</b> even with inline stuff</h2><h3>This is text that <i>should</i> remain</h3><h4>the <b>same</b> even with inline stuff</h4><h5>This is text that <i>should</i> remain</h5><h6>the <b>same</b> even with inline stuff</h6></div>",
        )

    def test_unordered_list_block(self):
        md = """

- This is text that _should_ remain
- the **same** even with inline stuff
- This is text that _should_ remain
- the **same** even with inline stuff
- This is text that _should_ remain
- the **same** even with inline stuff

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is text that <i>should</i> remain</li><li>the <b>same</b> even with inline stuff</li><li>This is text that <i>should</i> remain</li><li>the <b>same</b> even with inline stuff</li><li>This is text that <i>should</i> remain</li><li>the <b>same</b> even with inline stuff</li></ul></div>",
        )

    def test_ordered_list_block(self):
        md = """

1- This is text that _should_ remain
2- the **same** even with inline stuff
3- This is text that _should_ remain
4- the **same** even with inline stuff
5- This is text that _should_ remain
6- the **same** even with inline stuff

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is text that <i>should</i> remain</li><li>the <b>same</b> even with inline stuff</li><li>This is text that <i>should</i> remain</li><li>the <b>same</b> even with inline stuff</li><li>This is text that <i>should</i> remain</li><li>the <b>same</b> even with inline stuff</li></ol></div>",
        )

    def test_quote_block(self):
        md = """

>This is text that _should_ remain
>the **same** even with inline stuff
>This is text that _should_ remain

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is text that <i>should</i> remain the <b>same</b> even with inline stuff This is text that <i>should</i> remain</blockquote></div>",
        )

if __name__ == "__main__":
    unittest.main()
