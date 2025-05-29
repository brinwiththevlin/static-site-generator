"""HTMLNode tree representation of the content."""

from typing import override


class HTMLNode:
    """Class to represent an inline HTML node."""

    def __init__(
        self,
        value: str | None = None,
        tag: str | None = None,
        props: dict[str, str] | None = None,
        children: list["HTMLNode"] | None = None,
    ) -> None:
        """HTMLNode constructor.

        Args:
            value (str | None): text value of the node
            tag (str | None): tag name of the node
            props (dict[str, str] | None): dictionary of properties of the node
            children (list["HTMLNode"] | None): list of child nodes
        """
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list[HTMLNode] | None = children
        self.props: dict[str, str] | None = props

    def to_html(self) -> str:
        """To be implemented by child classes."""
        raise NotImplementedError

    def props_to_html(self) -> str:
        """Converts property dictionary to html string.

        Returns:
            html representation of the property dictionary
        """
        if self.props is None:
            return ""
        return " " + " ".join(f'{pair[0]}="{pair[1]}"' for pair in self.props.items())

    @override
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    @override
    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )


class LeafNode(HTMLNode):
    """class to represnt a HTML node that has a text value and no children."""

    def __init__(
        self,
        value: str,
        tag: str | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        """LeafNode constructor.

        Args:
            value (str): text value of the node
            tag (str | None): tag name of the node
            props (dict[str, str] | None): dictionary of properties of the node
        """
        super().__init__(value, tag, props, None)

    def to_html(self) -> str:
        """Convert node to html text.

        Returns:
            full html text representation of node

        Raises:
            ValueError: leaf node must have a value
        """
        if self.value is None:
            msg = "LeafNode must have value"
            raise ValueError(msg)

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """Parent nodes have no value and hsold have children."""

    def __init__(
        self,
        children: list["HTMLNode"],
        tag: str | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        """ParentNode constructor.

        Args:
            children (list["HTMLNode"]): list of child nodes
            tag (str | None): tag name of the node
            props (dict[str, str] | None): dictionary of properties of the node
        """
        super().__init__(None, tag, props, children)

    def to_html(self) -> str:
        """Convert node to html text.

        Returns:
            full html text representation of node

        Raises:
            ValueError: tag can not be None
            ValueError: children can not be None
        """
        if self.tag is None:
            msg = "tag can not be None"
            raise ValueError(msg)

        if not self.children:
            msg = "children can not be None"
            raise ValueError(msg)

        inner_html = "".join(x.to_html() for x in self.children)
        return f"<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>"
