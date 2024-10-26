# from textnode import TextNode, TextType

import logging
import os
import re
import shutil
from pathlib import Path

from block import markdown_to_html_node

logger = logging.getLogger(__name__)
logging.basicConfig(filename="out.log", level=logging.INFO)


print("hello world")


def dircopy(source: str | Path, dest: str | Path):
    """copy all content recursivly form one tree to the other

    deletes target file tree before the copy

    Args:
        source: path that is the root of the copy source tree
        dest: path thta is the root of the destination tree

    Raises:
        FileNotFoundError: if either path is a file and not a directory throw an FileNotFoundError
    """

    assert not os.path.isfile(source)
    assert not os.path.isfile(dest)
    if not os.path.exists(source):
        raise FileNotFoundError(f"{source} is not a directory")

    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    children = os.listdir(source)
    for child in children:
        if os.path.isdir(os.path.join(source, child)):
            dircopy(os.path.join(source, child), os.path.join(dest, child))
        else:
            logger.info(f"copying {os.path.join(source, child)} to {os.path.join(dest, child)}")
            shutil.copy(os.path.join(source, child), os.path.join(dest, child))


def extract_title(markdown: str) -> str:
    pattern = re.compile("^# (.*)")
    h1 = re.match(pattern, markdown)
    if not h1:
        raise Exception("no title to the markdown")

    return h1.group(1)


def generate_page(from_path: str | Path, template_path: str | Path, dest_path: str | Path):
    """generate an html page based on the template and teh source markdown storing at dest_path



    Args:
        from_path: source path for markdown
        template_path: template path containing html skeleton
        dest_path: path to write final html page
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as source:
        markdown = source.read()

    with open(template_path) as template:
        html_temp = template.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    full = html_temp.replace("{{ Title }}", title).replace("{{ Content }}", content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(full)


def main():
    """main function

    does everything
    """
    if os.getcwd().split("/")[-1] == "src":
        os.chdir("..")
    shutil.rmtree("public")

    source = os.path.join(os.getcwd(), "static")
    dest = os.path.join(os.getcwd(), "public")
    dircopy(source, dest)

    template_path = "template.html"
    content_path = "content/index.md"
    dest_path = "public/index.html"
    generate_page(content_path, template_path, dest_path)


if __name__ == "__main__":
    main()
