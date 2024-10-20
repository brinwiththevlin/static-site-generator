import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("this is a text node", TextType.BOLD)
        expected = "TextNode(this is a text node, bold, None)"
        self.assertEqual(str(node), expected)

    def test_diff_type(self):
        node = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("this is a text node", TextType.BOLD, "http://fake.url.com")
        node2 = TextNode("diff text node", TextType.BOLD, "http://fake.url.com")
        self.assertNotEqual(node, node2)

    def test_diff_url(self):
        node = TextNode("this is a text node", TextType.BOLD, "fake1.com")
        node2 = TextNode("this is a text node", TextType.BOLD, "fake2.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
