from htmlnode import HTMLNode

class ParentNode (HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("missing tag in ParentNode")
        if self.children == None:
            raise ValueError("missing children in Parentnode")
        props_str = self.props_to_html()
        if len(props_str) > 0:
            props_str = " " + props_str
        outhtml = f"<{self.tag}{props_str}>"
        for child in self.children:
            outhtml += child.to_html()
        outhtml += f"</{self.tag}>"
        return outhtml

