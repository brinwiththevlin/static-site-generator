import sys
import os

# Add the src/ directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = HTMLNode(props=props)
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(expected, node.props_to_html())

    def test_props_to_html_no_props(self):
        node = HTMLNode()
        expected = ""
        self.assertEqual(expected, node.props_to_html())

    def test_repr_no_child(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(tag="p", value="totally a paragraph", props=props)
        expected = f"HTMLNode(p, totally a paragraph, None, {props})"
        self.assertEqual(expected, str(node))

    def test_repr_child(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        child = HTMLNode(value="hello")
        node = HTMLNode(
            tag="p", value="totally a paragraph", children=[child], props=props
        )
        expected = "HTMLNode(p, totally a paragraph, [HTMLNode(None, hello, None, None)], {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(str(node), expected)

    def test_to_html(self):
        try:
            HTMLNode().to_html()
        except NotImplementedError:
            self.assertEqual(1, 1)
        else:
            self.fail()


class TestLeafNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = LeafNode("dummy", props=props)
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(expected, node.props_to_html())

    def test_reper_no_child(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = LeafNode(tag="p", value="totally a paragraph", props=props)
        expected = f"HTMLNode(p, totally a paragraph, None, {props})"
        self.assertEqual(expected, str(node))

    def test_repre_child(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        child = HTMLNode(value="hello")
        try:
            _ = LeafNode(
                tag="p",
                value="totally a paragraph",
                children=[child],  # type: ignore
                props=props,
            )
        except TypeError:
            self.assertEqual(1, 1)
        else:
            self.fail()

    def test_to_html_no_tag(self):
        node = LeafNode("this is a string")
        expected = "this is a string"
        self.assertEqual(node.to_html(), expected)

    def test_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = LeafNode("this is a string", tag="a", props=props)
        expected = (
            '<a href="https://www.google.com" target="_blank"> this is a string</a>'
        )
        self.assertEqual(node.to_html(), expected)

    def test_to_html_no_props(self):
        node = LeafNode("this is a string", tag="a")
        expected = "<a> this is a string</a>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_no_value(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = LeafNode(None, tag="a", props=props)  # type: ignore
        try:
            node.to_html()
        except ValueError:
            pass
        else:
            self.fail()


class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        leaf_node = LeafNode("this is a string", tag="a", props=props)
        node = ParentNode([leaf_node], None, None)
        try:
            node.to_html()
        except ValueError as e:
            if str(e) != "tag can not be None":
                self.fail()
        else:
            self.fail()

    def test_no_children(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = ParentNode(None, "div", props)  # type: ignore
        try:
            node.to_html()
        except ValueError as e:
            if str(e) != "children can not be None":
                self.fail()
        else:
            self.fail()

    def test_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        leaf_node = LeafNode("this is a string", tag="a", props=props)
        leaf_node2 = LeafNode("this is a string too", tag="a", props=props)
        node = ParentNode([leaf_node, leaf_node2], "div", None)
        expected = '<div><a href="https://www.google.com" target="_blank"> this is a string</a><a href="https://www.google.com" target="_blank"> this is a string too</a></div>'
        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
