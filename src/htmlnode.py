class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        string = ""
        if self.props != None:
            for key, value in self.props.items():
                string = f'{string} {key}="{value}"'
        return string
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=None, props=None):
        super().__init__(tag, value, children, props)
        
    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag == None:
            return f"{self.value}"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=None, props=None):
        super().__init__(tag, value, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("All parent nodes must have a value for tag.")
        elif self.children == None:
            raise ValueError("All parent nodes must have a value for children.")
        else:
            string = ""
            if len(self.children) == 0:
                return string
            else:
                for child in self.children:
                    string = f'{string}{child.to_html()}'
        return f'<{self.tag}{self.props_to_html()}>{string}</{self.tag}>'
    
    