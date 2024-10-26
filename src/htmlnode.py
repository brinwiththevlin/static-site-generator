class HTMLNode:
    """
    class to represent an inline HTML node
    """

    def __init__(
        self,
        value: str | None = None,
        tag: str | None = None,
        props: dict[str, str] | None = None,
        children: list["HTMLNode"] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """to be implemented by child classes"""
        raise NotImplementedError

    def props_to_html(self) -> str:
        """converts property dictionary to html string

        Returns:
            html representation of the property dictionary
        """
        if self.props is None:
            return ""
        return " " + " ".join(map(lambda pair: f'{pair[0]}="{pair[1]}"', self.props.items()))

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other: object, /) -> bool:
        assert isinstance(other, HTMLNode)
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )


class LeafNode(HTMLNode):
    """
    class to represnt a HTML node that has a text value and no children
    """

    def __init__(
        self,
        value: str,
        tag: str | None = None,
        props: dict[str, str] | None = None,
    ):
        super().__init__(value, tag, props, None)

    def to_html(self) -> str:
        """convert node to html text



        Returns:
            full html text representation of node

        Raises:
            ValueError: leaf node must have a value
        """
        if self.value is None:
            raise ValueError("LeafNode must have value")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """
    parent nodes have no value and hsold have children
    """

    def __init__(
        self,
        children: list["HTMLNode"],
        tag: str | None = None,
        props: dict[str, str] | None = None,
    ):
        super().__init__(None, tag, props, children)

    def to_html(self) -> str:
        """convert node to html text


        Returns:
            full html text representation of node

        Raises:
            ValueError: tag can not be None
            ValueError: children can not be None
        """
        if self.tag is None:
            raise ValueError("tag can not be None")

        if not self.children:
            raise ValueError("children can not be None")

        inner_html = "".join((map(lambda x: x.to_html(), self.children)))
        return f"<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>"
