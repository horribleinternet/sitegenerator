import unittest

from textnode import TextType, TextNode
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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
        old_nodes = [TextNode("there is some\n```\ncode\n```\nhere", TextType.NORMAL_TEXT)]
        nodes = split_nodes_delimiter(old_nodes, "```", TextType.CODE_TEXT)
        self.assertEqual(nodes, [TextNode("there is some\n", TextType.NORMAL_TEXT),
                                 TextNode("\ncode\n", TextType.CODE_TEXT),
                                 TextNode("\nhere", TextType.NORMAL_TEXT)])

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
