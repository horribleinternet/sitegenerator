import unittest

from textnode import TextType, TextNode
from markdown import split_nodes_delimiter

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
