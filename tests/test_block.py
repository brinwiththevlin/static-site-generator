import unittest

from block import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node


class TestBlock(unittest.TestCase):
    def test_one_block(self):
        markdown = "only one block of text"
        self.assertEqual([markdown], markdown_to_blocks(markdown))

    def test_multiple_blocks(self):
        markdown = "block one\n\nblock two\nhas two lines\n\nblock three"
        expected = ["block one", "block two\nhas two lines", "block three"]
        self.assertEqual(expected, markdown_to_blocks(markdown))

    def test_paragraph(self):
        markdown = "this is just a paragrapb\nnot special at all"
        expected = BlockType.PARAGRAPH
        self.assertEqual(expected, block_to_block_type(markdown))

    def test_quote(self):
        markdown = ">quote\n>still quote\n>last quote"
        expected = BlockType.QUOTE
        self.assertEqual(expected, block_to_block_type(markdown))

    def test_unordered(self):
        markdown = "* this is\n* an unordered\n* list"
        expected = BlockType.UL
        self.assertEqual(expected, block_to_block_type(markdown))

    def test_ordered(self):
        markdown = "1. this is\n2. an unordered\n3. list"
        expected = BlockType.OL
        self.assertEqual(expected, block_to_block_type(markdown))

    def test_header(self):
        markdown = "#### This is a header"
        expected = BlockType.HEADER
        self.assertEqual(expected, block_to_block_type(markdown))


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_header_conversion(self):
        # Test for headers with different levels
        markdown = "# Header 1\n\n## Header 2\n\n### Header 3"
        html_node = markdown_to_html_node(markdown)

        self.assertEqual(html_node.children[0].tag, "h1")  # type: ignore
        self.assertEqual(html_node.children[0].children[0].value, "Header 1")  # type: ignore
        self.assertEqual(html_node.children[1].tag, "h2")  # type: ignore
        self.assertEqual(html_node.children[1].children[0].value, "Header 2")  # type: ignore
        self.assertEqual(html_node.children[2].tag, "h3")  # type: ignore
        self.assertEqual(html_node.children[2].children[0].value, "Header 3")  # type: ignore

    def test_paragraph_conversion(self):
        # Test a single paragraph
        markdown = "This is a paragraph."
        html_node = markdown_to_html_node(markdown)

        self.assertEqual(html_node.children[0].tag, "p")  # type: ignore
        self.assertEqual(html_node.children[0].children[0].value, "This is a paragraph.")  # type: ignore

    def test_quote_conversion(self):
        # Test for a block quote
        markdown = "> This is a quote."
        html_node = markdown_to_html_node(markdown)

        self.assertEqual(html_node.children[0].tag, "blockquote")  # type: ignore
        self.assertEqual(html_node.children[0].children[0].value, "This is a quote.")  # type: ignore

    def test_unordered_list_conversion(self):
        # Test for an unordered list
        markdown = "* Item 1\n* Item 2\n* Item 3"
        html_node = markdown_to_html_node(markdown)

        self.assertEqual(html_node.children[0].tag, "ul")  # type: ignore
        self.assertEqual(html_node.children[0].children[0].tag, "li")  # type: ignore
        self.assertEqual(html_node.children[0].children[0].children[0].value, "Item 1")  # type: ignore
        self.assertEqual(html_node.children[0].children[1].tag, "li")  # type: ignore
        self.assertEqual(html_node.children[0].children[1].children[0].value, "Item 2")  # type: ignore
        self.assertEqual(html_node.children[0].children[2].tag, "li")  # type: ignore
        self.assertEqual(html_node.children[0].children[2].children[0].value, "Item 3")  # type: ignore

    def test_ordered_list_conversion(self):
        # Test for an ordered list
        markdown = "1. First item\n2. Second item\n3. Third item"
        html_node = markdown_to_html_node(markdown)

        self.assertEqual(html_node.children[0].tag, "ol")  # type: ignore
        self.assertEqual(html_node.children[0].children[0].tag, "li")  # type: ignore
        self.assertEqual(html_node.children[0].children[0].children[0].value, "First item")  # type: ignore
        self.assertEqual(html_node.children[0].children[1].tag, "li")  # type: ignore
        self.assertEqual(html_node.children[0].children[1].children[0].value, "Second item")  # type: ignore
        self.assertEqual(html_node.children[0].children[2].tag, "li")  # type: ignore
        self.assertEqual(html_node.children[0].children[2].children[0].value, "Third item")  # type: ignore

    def test_mixed_content_conversion(self):
        # Test for mixed content: headers, paragraphs, quotes, and lists
        markdown = "# Header\n\nThis is a paragraph.\n\n> A quote.\n\n* List item"
        html_node = markdown_to_html_node(markdown)

        self.assertEqual(html_node.children[0].tag, "h1")  # type: ignore
        self.assertEqual(html_node.children[0].children[0].value, "Header")  # type: ignore
        self.assertEqual(html_node.children[1].tag, "p")  # type: ignore
        self.assertEqual(html_node.children[1].children[0].value, "This is a paragraph.")  # type: ignore
        self.assertEqual(html_node.children[2].tag, "blockquote")  # type: ignore
        self.assertEqual(html_node.children[2].children[0].value, "A quote.")  # type: ignore
        self.assertEqual(html_node.children[3].tag, "ul")  # type: ignore
        self.assertEqual(html_node.children[3].children[0].tag, "li")  # type: ignore
        self.assertEqual(html_node.children[3].children[0].children[0].value, "List item")  # type: ignore


if __name__ == "__main__":
    unittest.main()
