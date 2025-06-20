
class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        return (self.tag == other.tag and self.value == other.value and
                self.children == other.children and self.props == other.props)

    def to_html(self):
        raise NotImplementedError("HTMLNode.to_html not implementd")

    def props_to_html(self):
        if self.props == None or len(self.props) == 0:
            return ""
        prop_list = list(map(lambda x: f'{x[0]}="{x[1]}"', self.props.items()))
        return " " + " ".join(prop_list)

    def children_to_html(self):
        childrenstr = ""
        for child in self.children:
            childrenstr += child.__repl__()
        return childrenstr


    def __repl__(self):
        tag = f"<{tag} {self.props_to_html}>{self.value} {self.children_to_html()} </{tag}>"
