import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = HTMLNode(props=props)
        expected = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(expected, node.props_to_html())

    def test_reper_no_child(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(tag="<p>", value="totally a paragraph", props=props)
        expected = f"HTMLNode(<p>, totally a paragraph, None, {props}"
        self.assertEqual(expected, str(node))

    def test_repre_child(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        child = HTMLNode(value="hello")
        node = HTMLNode(
            tag="<p>", value="totally a paragraph", children=[child], props=props
        )
        expected = "HTMLNode(<p>, totally a paragraph, [HTMLNode(None, hello, None, None], {'href': 'https://www.google.com', 'target': '_blank'}"
        self.assertEqual(str(node), expected)

    def test_to_html(self):
        try:
            HTMLNode().to_html()
        except NotImplementedError:
            self.assertEqual(1, 1)
        else:
            self.fail()


if __name__ == "__main__":
    unittest.main()
