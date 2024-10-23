from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        if text_type not in TextType:
            raise ValueError("text type must be in TextType")
        self.text = text
        self.text_type = text_type
        if text_type == TextType.LINK or text_type == TextType.IMAGE:
            if not url:
                raise ValueError("link or image requires a url")
            self.url = url
        elif url is not None:
            raise ValueError("only link or image take a url")
        else:
            self.url = None

    def __eq__(self, other: object, /) -> bool:
        assert isinstance(other, TextNode)
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
