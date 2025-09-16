"""Main module for the static site generator."""

import logging
import os
import re
import shutil
import sys
from pathlib import Path

from ssg.block import markdown_to_html_node

logger = logging.getLogger(__name__)
logging.basicConfig(filename="out.log", level=logging.INFO)


def dircopy(source: str | Path, dest: str | Path) -> None:
    """Copy all content recursively from one tree to the other.

    Deletes the target file tree before the copy.

    Args:
        source (str | Path): Path that is the root of the copy source tree.
        dest (str | Path): Path that is the root of the destination tree.

    Raises:
        FileNotFoundError: If either path is a file and not a directory.
    """
    if not Path(source).is_dir() or not Path(source).exists():
        raise FileNotFoundError(f"{source} is not a directory")
    if Path(dest).exists() and not Path(dest).is_dir():
        logger.info(f"{dest} is not a directory")
        raise FileNotFoundError(f"{dest} is not a directory")

    if Path(dest).exists():
        shutil.rmtree(dest)
    Path(dest).mkdir(parents=True, exist_ok=True)

    children = Path(source).iterdir()
    for child in children:
        if child.is_dir():
            # dircopy using Pathlib
            dircopy(child, Path(dest) / child.name)
        else:
            logger.info(f"copying {child} to {Path(dest) / child.name}")
            _ = shutil.copy(child, Path(dest) / child.name)


def extract_title(markdown: str) -> str:
    """Extract the title from the markdown file.

    The title is the first line of the markdown file, and it is expected to be in the format "# Title".

    Args:
        markdown (str): The markdown content.

    Returns:
        str: The title extracted from the markdown content.

    Raises:
        Exception: If the title is not found in the markdown content.
    """
    pattern = re.compile("^# (.*)")
    h1 = re.match(pattern, markdown)
    if not h1:
        exc = Exception("Title not found in markdown")
        raise exc

    return h1.group(1)


def generate_page(
    from_path: str | Path,
    template_path: str | Path,
    dest_path: str | Path,
    base_path: str | Path,
) -> None:
    """Generate an html page based on the template and teh source markdown storing at dest_path.

    Args:
        from_path: source path for markdown
        template_path: template path containing html skeleton
        dest_path: path to write final html page
        base_path: base path for the site
    """
    logger.info(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # open with Path.open
    with Path(from_path).open() as source:
        markdown = source.read()

    with Path(template_path).open() as template:
        html_temp = template.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    full = html_temp.replace("{{ Title }}", title).replace("{{ Content }}", content)

    full = full.replace('href="/', f'href="{base_path}/').replace('src="/', f'src="{base_path}/')

    Path(dest_path).parent.mkdir(exist_ok=True, parents=True)
    with Path(dest_path).open("w") as file:
        _ = file.write(full)


def generate_pages_recursive(
    dir_path_content: str | Path,
    template_path: str | Path,
    dest_dir_path: str | Path,
    base_path: str | Path,
) -> None:
    """Generates html pages recursively from a directory containing markdown files.

    This function will create a directory tree in the desination directory

    Args:
        dir_path_content: path where the md content lives
        template_path: path where the html template lives
        dest_dir_path: path to put all html pages in
        base_path: base path for the site
    """
    children = Path(dir_path_content).iterdir()
    for child in children:
        if child.name.endswith(".md"):
            generate_page(
                child, template_path, Path(dest_dir_path) / child.name.replace(".md", ".html"), Path(base_path)
            )
        if child.is_dir():
            generate_pages_recursive(child, template_path, Path(dest_dir_path) / child.name, Path(base_path))


def main() -> None:
    """Main function.

    does everything
    """
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    if not base_path.startswith("/"):
        base_path = "/" + base_path
    if not base_path.endswith("/"):
        base_path = base_path + "/"

    if Path.cwd().name == "ssg":
        os.chdir("..")
    if Path("docs").exists():
        shutil.rmtree("docs")

    base_dir = Path.cwd()
    if base_dir.name == "src":
        base_dir = base_dir.parent
    source = base_dir / Path("static")
    dest = base_dir / Path("docs")
    dircopy(source, dest)

    template_path = "template.html"
    content_path = "content"
    dest_path = "docs"
    generate_pages_recursive(content_path, template_path, dest_path, base_path)


if __name__ == "__main__":
    main()
