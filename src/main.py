# from textnode import TextNode, TextType

import logging
import os
import shutil
from pathlib import Path

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


def main():
    """main function

    does everything
    """
    source = "static"
    dest = "public"
    if os.getcwd().split("/")[-1] == "src":
        source = os.path.join(os.getcwd(), "..", source)
        dest = os.path.join(os.getcwd(), "..", dest)
    else:
        source = os.path.join(os.getcwd(), source)
        dest = os.path.join(os.getcwd(), dest)

    dircopy(source, dest)


if __name__ == "__main__":
    main()
