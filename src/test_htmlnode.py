import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_prop_1(self):
        props = {"href": "https://www.google.com"}
        node = HTMLNode(None, None, None, props)
        self.assertEqual(node.props_to_html(), 'href = "https://www.google.com"')

    def test_props_3(self):
        props = {"href": "https://www.google.com", "target": "_blank", "stuff": "wow"}
        node = HTMLNode(None, None, None, props)
        self.assertEqual(node.props_to_html(), 'href = "https://www.google.com" target = "_blank" stuff = "wow"')

    def test_eq(self):
        props = {"href": "https://www.google.com", "target": "_blank", "stuff": "wow"}
        node1 = HTMLNode("img", "what.jpg", None, props)
        node2 = HTMLNode("img", "what.jpg", None, props)
        self.assertEqual(node1, node2)
