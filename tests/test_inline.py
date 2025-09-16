import unittest

from ssg.htmlnode import LeafNode
from ssg.inline import (  # split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)
from ssg.textnode import TextNode, TextType


class TestToHTMLNode(unittest.TestCase):
    def test_text(self):
        text_node = TextNode("words", TextType.TEXT)
        leaf_node = LeafNode("words")
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)

    def test_bold(self):
        text_node = TextNode("words", TextType.BOLD)
        leaf_node = LeafNode("words", "b")
        self.assertEqual(leaf_node, text_node_to_html_node(text_node))

    def test_italic(self):
        text_node = TextNode("words", TextType.ITALIC)
        leaf_node = LeafNode("words", "i")
        self.assertEqual(leaf_node, text_node_to_html_node(text_node))

    def test_code(self):
        text_node = TextNode("words", TextType.CODE)
        leaf_node = LeafNode("words", "code")
        self.assertEqual(leaf_node, text_node_to_html_node(text_node))

    def test_link(self):
        text_node = TextNode("words", TextType.LINK, "url")
        leaf_node = LeafNode("words", "a", {"href": "url"})
        self.assertEqual(leaf_node, text_node_to_html_node(text_node))

    def test_image(self):
        text_node = TextNode("words", TextType.IMAGE, "url")
        leaf_node = LeafNode("", "img", {"src": "url", "alt": "words"})
        self.assertEqual(leaf_node, text_node_to_html_node(text_node))

    def test_empty_text(self):
        """Test conversion with empty text."""
        text_node = TextNode("", TextType.TEXT)
        leaf_node = LeafNode("")
        self.assertEqual(leaf_node, text_node_to_html_node(text_node))

    def test_empty_link(self):
        """Test link node with missing URL."""
        try:
            text_node = TextNode("link", TextType.LINK)  # Missing URL
            text_node_to_html_node(text_node)
        except ValueError:
            pass
        else:
            self.fail()

    def test_empty_image(self):
        """Test image node with missing URL."""
        try:
            text_node = TextNode("alt", TextType.IMAGE)  # Missing URL
            text_node_to_html_node(text_node)
        except ValueError:
            pass
        else:
            self.fail()


class TestDelimeterSplit(unittest.TestCase):
    def test_split_bold(self):
        node = TextNode("this text **is** bold **here**", TextType.TEXT)
        expected = [
            TextNode("this text ", TextType.TEXT),
            TextNode("is", TextType.BOLD),
            TextNode(" bold ", TextType.TEXT),
            TextNode("here", TextType.BOLD),
        ]
        output = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(expected, output)

    def test_no_split(self):
        node = TextNode("no bold here", TextType.TEXT)
        self.assertEqual([node], split_nodes_delimiter([node], "**", TextType.BOLD))

    def test_wrong_delimiter(self):
        node = TextNode("no bold here", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.BOLD)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", "help")  # type: ignore # Invalid TextType

    def test_empty_node(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual([], split_nodes_delimiter([node], "**", TextType.BOLD))

    def test_delimiter_at_start(self):
        node = TextNode("**bold at start** normal", TextType.TEXT)
        expected = [
            TextNode("bold at start", TextType.BOLD),
            TextNode(" normal", TextType.TEXT),
        ]
        output = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(expected, output)

    def test_delimiter_at_end(self):
        node = TextNode("normal **bold at end**", TextType.TEXT)
        expected = [
            TextNode("normal ", TextType.TEXT),
            TextNode("bold at end", TextType.BOLD),
        ]
        output = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(expected, output)

    def test_delimiter_empty_content(self):
        node = TextNode("empty ** ** content", TextType.TEXT)
        expected = [
            TextNode("empty ", TextType.TEXT),
            TextNode(" content", TextType.TEXT),
        ]
        output = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(expected, output)

    def test_multiple_delimiters(self):
        node = TextNode("**bold** and **another bold**", TextType.TEXT)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD),
        ]
        output = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(expected, output)

    def test_mixed_delimiters(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        bold_split = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_bold = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and _italic_", TextType.TEXT),
        ]
        self.assertEqual(expected_bold, bold_split)

        italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)
        expected_mixed = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(expected_mixed, italic_split)


class TestExtract(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        text = "This is an image ![alt_text](http://image-url.com/image.png)"
        expected = [("alt_text", "http://image-url.com/image.png")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_multiple(self):
        text = "![alt1](http://url1.com/image1.png) and ![alt2](http://url2.com/image2.png)"
        expected = [
            ("alt1", "http://url1.com/image1.png"),
            ("alt2", "http://url2.com/image2.png"),
        ]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_no_images(self):
        text = "This text has no images."
        expected = []
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_edge_cases(self):
        text = "![](http://url.com/emptyalt.png) ![alt_only]()"
        expected = [("", "http://url.com/emptyalt.png"), ("alt_only", "")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_single(self):
        text = "This is a [link](http://example.com)"
        expected = [("link", "http://example.com")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_multiple(self):
        text = "[link1](http://example1.com) and [link2](http://example2.com)"
        expected = [("link1", "http://example1.com"), ("link2", "http://example2.com")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_no_links(self):
        text = "This text has no links."
        expected = []
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_edge_cases(self):
        text = "[](http://url.com/emptyanchor) [anchor_only]()"
        expected = [("", "http://url.com/emptyanchor"), ("anchor_only", "")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_image(self):
        text = "![](http://url.com/emptyalt.png)"
        expected = []
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)


class TestNonDelimSplit(unittest.TestCase):
    def test_no_images(self):
        old_nodes = [TextNode("This is a simple text without any links.", TextType.TEXT)]
        result = split_nodes_image(old_nodes)
        expected = [TextNode("This is a simple text without any links.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_single_image(self):
        old_nodes = [
            TextNode(
                "Here is a link ![image](http://example.com/image.png) in text.",
                TextType.TEXT,
            )
        ]
        result = split_nodes_image(old_nodes)
        expected = [
            TextNode("Here is a link ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "http://example.com/image.png"),
            TextNode(" in text.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        old_nodes = [
            TextNode(
                "Image one ![image1](http://example.com/img1.png) and image two ![image2](http://example.com/img2.png).",
                TextType.TEXT,
            )
        ]
        result = split_nodes_image(old_nodes)
        expected = [
            TextNode("Image one ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "http://example.com/img1.png"),
            TextNode(" and image two ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "http://example.com/img2.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_only(self):
        old_nodes = [
            TextNode("This is the first text node.", TextType.TEXT),
            TextNode("This is the second text node.", TextType.TEXT),
        ]
        result = split_nodes_image(old_nodes)
        expected = [
            TextNode("This is the first text node.", TextType.TEXT),
            TextNode("This is the second text node.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_empty_node(self):
        old_nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_image(old_nodes)
        expected = []  # Empty node should result in an empty list
        self.assertEqual(result, expected)

    def test_image_at_start(self):
        old_nodes = [
            TextNode(
                "![image](http://example.com/image.png) is the first thing.",
                TextType.TEXT,
            )
        ]
        result = split_nodes_image(old_nodes)
        expected = [
            TextNode("image", TextType.IMAGE, "http://example.com/image.png"),
            TextNode(" is the first thing.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_image_at_end(self):
        old_nodes = [
            TextNode(
                "the image is last ![image](http://example.com/image.png)",
                TextType.TEXT,
            )
        ]
        result = split_nodes_image(old_nodes)
        expected = [
            TextNode("the image is last ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "http://example.com/image.png"),
        ]
        self.assertEqual(result, expected)

    def test_no_links(self):
        old_nodes = [TextNode("This is a simple text without any links.", TextType.TEXT)]
        result = split_nodes_link(old_nodes)
        expected = [TextNode("This is a simple text without any links.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_single_link(self):
        old_nodes = [
            TextNode(
                "Here is a link [link](http://example.com/link.png) in text.",
                TextType.TEXT,
            )
        ]
        result = split_nodes_link(old_nodes)
        expected = [
            TextNode("Here is a link ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://example.com/link.png"),
            TextNode(" in text.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        old_nodes = [
            TextNode(
                "Image one [link1](http://example.com/img1.png) and link two [link2](http://example.com/img2.png).",
                TextType.TEXT,
            )
        ]
        result = split_nodes_link(old_nodes)
        expected = [
            TextNode("Image one ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "http://example.com/img1.png"),
            TextNode(" and link two ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "http://example.com/img2.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_only_link(self):
        old_nodes = [
            TextNode("This is the first text node.", TextType.TEXT),
            TextNode("This is the second text node.", TextType.TEXT),
        ]
        result = split_nodes_link(old_nodes)
        expected = [
            TextNode("This is the first text node.", TextType.TEXT),
            TextNode("This is the second text node.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_empty_node_link(self):
        old_nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_link(old_nodes)
        expected = []  # Empty node should result in an empty list
        self.assertEqual(result, expected)

    def test_link_at_start(self):
        old_nodes = [
            TextNode(
                "[link](http://example.com/link.png) is the first thing.",
                TextType.TEXT,
            )
        ]
        result = split_nodes_link(old_nodes)
        expected = [
            TextNode("link", TextType.LINK, "http://example.com/link.png"),
            TextNode(" is the first thing.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_link_at_end(self):
        old_nodes = [
            TextNode(
                "the link is last [link](http://example.com/link.png)",
                TextType.TEXT,
            )
        ]
        result = split_nodes_link(old_nodes)
        expected = [
            TextNode("the link is last ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://example.com/link.png"),
        ]
        self.assertEqual(result, expected)


class TestTextToTextNodes(unittest.TestCase):
    def test(self):
        text = "This is **text** with an _italic_ word and a ```code block``` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
