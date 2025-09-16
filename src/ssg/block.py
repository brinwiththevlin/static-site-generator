"""Handles markdown Blocks and converts them to HTMLNode tree representation."""

import re
from enum import Enum

from ssg.htmlnode import HTMLNode, ParentNode
from ssg.inline import text_node_to_html_node, text_to_textnodes


class BlockType(Enum):
    """BlockType is an enumeration that represents the type of block in a markdown file.

    Attributes:
        HEADER (str): Header block type.
        UL (str): unordered list block type.
        OL (srt): ordered list block type.
        QUOTE (str): quote block type.
        PARAGRAPH (str): Paragraph block type.
    """

    HEADER = "header"
    UL = "unorderd"
    OL = "ordered"
    QUOTE = "quote"
    PARAGRAPH = "paragraph"


def markdown_to_blocks(markdown: str) -> list[str]:
    """Takes a string that represents a whole block.

    A markdown file is understood to be a collection of blocks separated by an empty line

    Args:
        markdown: the full text of a markdown file

    Returns:
        list of strings each representing a block in the original
    """
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks]


def block_to_block_type(block: str) -> BlockType:
    r"""Takes a single markdown block and performs pattern mattching to return the type of block it is.

    starting with 1-6 # is a header
    each line starting with > is a quote
    each line starting with \* or - is unordered list
    \d\. at the start of every line is an ordered list
    else just a paragraph

    Args:
        block: original block

    Returns:
        block type
    """
    pattern = re.compile(r"^#{1,6} ")
    if re.match(pattern, block):
        return BlockType.HEADER
    lines = block.split("\n")
    if all(x[0] == ">" for x in lines):
        return BlockType.QUOTE
    if all(x[0] == "*" for x in lines) or all(x[0] == "-" for x in lines):
        return BlockType.UL

    pattern = re.compile(r"^\s*\d\.")
    if all(re.match(pattern, x) for x in lines):
        return BlockType.OL
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> ParentNode:
    """Takes a whole md file and converts it to the HTMLNode tree representation of the content.

    Args:
        markdown: full md file

    Returns:
        single HTMLNode that is the head of the HTMLNode tree for the content
    """
    blocks = markdown_to_blocks(markdown)
    block_nodes: list[HTMLNode] = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADER:
                hashtag, head = block.split(maxsplit=1)
                tag = f"h{len(hashtag)}"
                children = list(map(text_node_to_html_node, text_to_textnodes(head)))
                block_nodes.append(ParentNode(tag=tag, children=children))
            case BlockType.PARAGRAPH:
                children = list(map(text_node_to_html_node, text_to_textnodes(block)))
                block_nodes.append(ParentNode(tag="p", children=children))
            case BlockType.QUOTE:
                quote = "\n".join(map(str.strip, block.replace(">", "").split("\n")))
                children = list(map(text_node_to_html_node, text_to_textnodes(quote)))
                block_nodes.append(ParentNode(tag="blockquote", children=children))
            case BlockType.UL:
                list_items = block.split("\n* ")
                if list_items[0] == block:
                    list_items = block.split("\n- ")
                list_items = [re.sub(r"^[-\*] ", "", item) for item in list_items if item != ""]
                list_item_nodes: list[HTMLNode] = []
                for item in list_items:
                    children = list(map(text_node_to_html_node, text_to_textnodes(item)))
                    list_item_nodes.append(ParentNode(tag="li", children=children))
                block_nodes.append(ParentNode(tag="ul", children=list_item_nodes))
            case BlockType.OL:
                block = re.sub(r"[\n]?\d+\. ", "|%<~DEL~>%|", block)  # noqa: PLW2901
                list_items = block.split("|%<~DEL~>%|")
                list_items = [item for item in list_items if item != ""]
                list_item_nodes = []
                for item in list_items:
                    children = list(map(text_node_to_html_node, text_to_textnodes(item)))
                    list_item_nodes.append(ParentNode(tag="li", children=children))
                block_nodes.append(ParentNode(tag="ol", children=list_item_nodes))

    return ParentNode(tag="div", children=block_nodes)
