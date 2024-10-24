import os
import sys

# Add the src/ directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("this is a text node", TextType.BOLD)
        expected = "TextNode(this is a text node, TextType.BOLD, None)"
        self.assertEqual(str(node), expected)

    def test_diff_type(self):
        node = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.LINK, "url")
        self.assertNotEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("this is a text node", TextType.LINK, "http://fake.url.com")
        node2 = TextNode("diff text node", TextType.LINK, "http://fake.url.com")
        self.assertNotEqual(node, node2)

    def test_diff_url(self):
        node = TextNode("this is a text node", TextType.LINK, "fake1.com")
        node2 = TextNode("this is a text node", TextType.LINK, "fake2.com")
        self.assertNotEqual(node, node2)

    def test_link_no_url(self):
        try:
            _ = TextNode("this is a text node", TextType.LINK)
        except ValueError:
            pass
        else:
            self.fail()

    def test_unexpected_text_type(self):
        try:
            _ = TextNode("this is a test", "normal", "fake url")  # type: ignore
        except ValueError:
            pass
        else:
            self.fail()

    def test_unexpected_url(self):
        try:
            _ = TextNode("this is a text node", TextType.BOLD, "fake1.com")
        except ValueError:
            pass
        else:
            self.fail()


if __name__ == "__main__":
    unittest.main()
