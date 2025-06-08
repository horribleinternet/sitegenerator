import unittest

from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()
