from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            #print(f"*** {self.tag} ***")
            #print(f"*** {self.props} ***")
            raise ValueError("LeafNode contains no value")
        if self.tag == None:
            return self.value
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
