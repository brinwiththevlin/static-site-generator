import re
from enum import Enum

from htmlnode import HTMLNode, ParentNode
from inline import text_node_to_html_node, text_to_textnodes


class BlockType(Enum):
    HEADER = "header"
    UL = "unorderd"
    OL = "ordered"
    QUOTE = "quote"
    PARAGRAPH = "paragraph"


def markdown_to_blocks(markdown: str) -> list[str]:
    """takes a string that represents a whole block


    a markdown file is understood to be a collection of blocks separated by an empty line

    Args:
        markdown: the full text of a markdown file

    Returns:
        list of strings each representing a block in the original
    """
    blocks = markdown.split("\n\n")
    return list(map(lambda x: x.strip(), blocks))


def block_to_block_type(block: str) -> BlockType:
    """takes a single markdown block and performs pattern mattching to return the type of block it is

    starting with 1-6 # is a header
    each line starting with > is a quote
    each line starting with * or - is unordered list
    \\d\\. at the start of every line is an ordered list
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
    if all(map(lambda x: x[0] == ">", lines)):
        return BlockType.QUOTE
    if all(map(lambda x: x[0] == "*", lines)) or all(map(lambda x: x[0] == "-", lines)):
        return BlockType.UL

    pattern = re.compile(r"^\s*\d\.")
    if all(map(lambda x: re.match(pattern, x), lines)):
        return BlockType.OL
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> ParentNode:
    """takes a whole md file and converts it to the HTMLNode tree representation of the content

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
                quote = block.replace("> ", "")
                children = list(map(text_node_to_html_node, text_to_textnodes(quote)))
                block_nodes.append(ParentNode(tag="blockquote", children=children))
            case BlockType.UL:
                list_items = block.split("\n* ")
                if list_items[0] == block:
                    list_items = block.split("\n- ")
                list_items = [re.sub(r"^[-\*] ", "", item) for item in list_items if item != ""]
                list_item_nodes = []
                for item in list_items:
                    children = list(map(text_node_to_html_node, text_to_textnodes(item)))
                    list_item_nodes.append(ParentNode(tag="li", children=children))
                block_nodes.append(ParentNode(tag="ul", children=list_item_nodes))
            case BlockType.OL:
                block = re.sub(r"[\n]?\d+\. ", "|%<~DEL~>%|", block)
                list_items = block.split("|%<~DEL~>%|")
                list_items = [item for item in list_items if item != ""]
                list_item_nodes = []
                for item in list_items:
                    children = list(map(text_node_to_html_node, text_to_textnodes(item)))
                    list_item_nodes.append(ParentNode(tag="li", children=children))
                block_nodes.append(ParentNode(tag="ol", children=list_item_nodes))

    tree = ParentNode(tag="div", children=block_nodes)
    return tree
