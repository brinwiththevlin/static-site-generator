"""Handles the conversion of inline tags to HTML."""

import re

from ssg.htmlnode import HTMLNode, LeafNode
from ssg.textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    """Convert a TextNode to a HTMLNode.

    used the TextType of a TextNode to generate a new HTMLNode

    Args:
        text_node: the TextNode to convert

    Returns:
        HTMLNode: the associated HTMLNode
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(text_node.text)
        case TextType.BOLD:
            return LeafNode(text_node.text, "b")
        case TextType.ITALIC:
            return LeafNode(text_node.text, "i")
        case TextType.CODE:
            return LeafNode(text_node.text, "code")
        case TextType.LINK:
            if text_node.url is None:
                msg = "Link requires a url"
                raise ValueError(msg)
            return LeafNode(text_node.text, "a", props={"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url is None:
                msg = "Image requires a url"
                raise ValueError(msg)
            return LeafNode("", "img", props={"src": text_node.url, "alt": text_node.text})


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """Creates new list of TextNodes with appropriate TextType.

    takes a list of TextNodes and a delimiter and splits each TextNode by the delimter and changes
    the appropriate parts to the target TextTypei

    Args:
        old_nodes: original list of nodes
        delimiter: delimiter to split on
        text_type: target TextType

    Returns:
        new list of shorter TextNodes labeled appropriately

    Raises:
        ValueError: if text_type not in delim_dic or the delimiter is the wrong one
    """
    delim_dic = {
        TextType.BOLD: "**",
        TextType.ITALIC: "_",
        TextType.CODE: "`",
    }

    if text_type not in delim_dic:
        raise ValueError(f"the accepted text_type must be one of {delim_dic.keys()}")
    if delim_dic[text_type] != delimiter:
        raise ValueError(f"the delimiter for {text_type} is {delim_dic[text_type]}")

    if len(old_nodes) == 0:
        return []

    first, rest = old_nodes[0], old_nodes[1:]
    if first.text == "":
        return []

    mod = int(first.text.find(delimiter) == 0)
    parts = first.text.split(delimiter)

    if len(parts) == 1:
        return [first, *split_nodes_delimiter(rest, delimiter, text_type)]
    if parts[0] == "":
        parts = parts[1:]
    if parts[-1] == "":
        parts = parts[:-1]

    new_nodes = [
        TextNode(a, TextType.TEXT, first.url) if i % 2 == mod else TextNode(a, text_type, first.url)
        for i, a in enumerate(parts)
        if a.strip() != ""
    ]
    new_nodes.extend(split_nodes_delimiter(rest, delimiter, text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """Takes in raw Markdown text and return a list of tuples.

    eack image if of the format ![alt_text](url) and it transformed into a tuple (alt_text, url)

    Args:
        text: raw text

    Returns:
        list of alt_text, url tuples
    """
    pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Takes in raw Markdown text and returns a list of tuples for links.

    each link is of the format [anchor_text](url). this is then transformed into a tuple (anchor_text,url)

    Args:
    text: raw markdown text

    Returns:
    list of (anchor_text, url) tuples
    """
    pattern = re.compile(r"\[(.*?)\]\((.*?)\)")
    return re.findall(pattern, text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """Splits TextNodes so that image test is its own node of TextType.IMAGE.

    Args:
        old_nodes: old list of TextNodes
    Returns:
        longer list split appropriately
    """
    if len(old_nodes) == 0:
        return []

    first, rest = old_nodes[0], old_nodes[1:]
    if first.text == "":
        return []

    matches = extract_markdown_images(first.text)
    new_string = re.sub(r"!\[(.*?)\]\((.*?)\)", "|%<~DEL~>%| |%<~DEL~>%|", first.text)
    parts = [part for part in new_string.split("|%<~DEL~>%|") if part != ""]

    if not matches:
        return [first, *split_nodes_image(rest)]

    new_nodes = []
    while matches or parts:
        if parts[0] == " ":
            pair = matches.pop(0)
            new_nodes.append(TextNode(pair[0], TextType.IMAGE, pair[1]))
            _ = parts.pop(0)
        else:
            new_nodes.append(TextNode(parts.pop(0), TextType.TEXT))
    return new_nodes + split_nodes_image(rest)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """Splits TextNodes so that image test is its own node of TextType.IMAGE.

    Args:
        old_nodes: old list of TextNodes
    Returns:
        longer list split appropriately
    """
    if len(old_nodes) == 0:
        return []

    first, rest = old_nodes[0], old_nodes[1:]
    if first.text == "":
        return []

    matches = extract_markdown_links(first.text)
    new_string = re.sub(r"\[(.*?)\]\((.*?)\)", "|%<~DEL~>%| |%<~DEL~>%|", first.text)
    parts = [part for part in new_string.split("|%<~DEL~>%|") if part != ""]

    if not matches:
        return [first, *split_nodes_link(rest)]

    new_nodes = []
    while matches or parts:
        if parts[0] == " ":
            pair = matches.pop(0)
            new_nodes.append(TextNode(pair[0], TextType.LINK, pair[1]))
            _ = parts.pop(0)
        else:
            new_nodes.append(TextNode(parts.pop(0), TextType.TEXT))
    return new_nodes + split_nodes_link(rest)


def text_to_textnodes(text: str) -> list[TextNode]:
    """Converts a string to a list of TextNodes.

    The string is split by spaces and each part is converted to a TextNode.

    Args:
        text: the string to convert
    Returns:
        list of TextNodes
    """
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    return split_nodes_link(nodes)
