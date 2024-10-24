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
