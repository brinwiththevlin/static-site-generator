import unittest

from src.textnode import TextType, TextNode
from src.htmlnode import LeafNode
from src.utils import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
)


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
        """Test split on an empty TextNode."""
        node = TextNode("", TextType.TEXT)
        self.assertEqual([], split_nodes_delimiter([node], "**", TextType.BOLD))

    def test_delimiter_at_start(self):
        """Test delimiter at the start of text."""
        node = TextNode("**bold at start** normal", TextType.TEXT)
        expected = [
            TextNode("bold at start", TextType.BOLD),
            TextNode(" normal", TextType.TEXT),
        ]
        output = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(expected, output)

    def test_delimiter_at_end(self):
        """Test delimiter at the end of text."""
        node = TextNode("normal **bold at end**", TextType.TEXT)
        expected = [
            TextNode("normal ", TextType.TEXT),
            TextNode("bold at end", TextType.BOLD),
        ]
        output = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(expected, output)

    def test_delimiter_empty_content(self):
        """Test delimiter with empty content between."""
        node = TextNode("empty ** ** content", TextType.TEXT)
        expected = [
            TextNode("empty ", TextType.TEXT),
            TextNode(" content", TextType.TEXT),
        ]
        output = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(expected, output)

    def test_multiple_delimiters(self):
        """Test multiple delimiters in the same node."""
        node = TextNode("**bold** and **another bold**", TextType.TEXT)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD),
        ]
        output = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(expected, output)

    def test_mixed_delimiters(self):
        """Test mixing different delimiters."""
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        bold_split = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_bold = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and *italic*", TextType.TEXT),
        ]
        self.assertEqual(expected_bold, bold_split)

        italic_split = split_nodes_delimiter(bold_split, "*", TextType.ITALIC)
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


if __name__ == "__main__":
    unittest.main()
