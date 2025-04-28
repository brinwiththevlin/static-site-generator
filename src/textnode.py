"""textnode tree representation of the content."""

from enum import Enum
from typing import final, override


class TextType(Enum):
    """text type Enum inline text can only be one of these types.

    Attributes:
        TEXT (str): normal text
        BOLD (str): bold text
        ITALIC (str): italic
        CODE (str): code block
        LINK (str): hyperlink
        IMAGE (str): image and alt text
    """

    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


@final
class TextNode:
    """text node that contains text information, text type can only be one of TextType."""

    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        """Initialize a text node.

        Args:
            text: the text in the node
            text_type: the type of text
            url: the url for link or image, if applicable
        """
        if text_type not in TextType:
            msg = "text type must be in TextType"
            raise ValueError(msg)
        self.text = text
        self.text_type = text_type
        if text_type in (TextType.LINK, TextType.IMAGE):
            if not url:
                msg = "link or image requires a url"
                raise ValueError(msg)
            self.url = url
        elif url is not None:
            msg = "only link or image take a url"
            raise ValueError(msg)
        else:
            self.url = None

    @override
    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    @override
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
