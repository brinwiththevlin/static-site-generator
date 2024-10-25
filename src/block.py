import re


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


def block_to_block_type(block: str) -> str:
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
        return "header"
    lines = block.split("\n")
    if all(map(lambda x: x[0] == ">", lines)):
        return "quote"
    if all(map(lambda x: x[0] == "*", lines)) or all(map(lambda x: x[0] == "-", lines)):
        return "unordered list"

    pattern = re.compile(r"^\s*\d\.")
    if all(map(lambda x: re.match(pattern, x), lines)):
        return "ordered list"
    return "paragraph"
