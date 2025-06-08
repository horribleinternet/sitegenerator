from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode contains no value")
        if self.tag == None:
            return self.value
        props_str = self.props_to_html()
        if len(props_str) > 0:
            props_str = " " + props_str
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}"
