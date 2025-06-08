import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_prop_1(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href = "https://www.google.com">Click me!</a>')

    def test_leaf_props_3(self):
        props = {"href": "https://www.google.com", "target": "_blank", "stuff": "wow"}
        node = LeafNode("a", "Click me!", props)
        self.assertEqual(node.to_html(), '<a href = "https://www.google.com" target = "_blank" stuff = "wow">Click me!</a>')

    def test_leaf_value(self):
        node = LeafNode(None, "Read me!")
        self.assertEqual(node.to_html(), "Read me!")
    
