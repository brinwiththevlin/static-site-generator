import unittest

from block import block_to_block_type, markdown_to_blocks


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
        expected = "paragraph"
        self.assertEqual(expected, block_to_block_type(markdown))

    def test_quote(self):
        markdown = ">quote\n>still quote\n>last quote"
        expected = "quote"
        self.assertEqual(expected, block_to_block_type(markdown))

    def test_unordered(self):
        markdown = "* this is\n* an unordered\n* list"
        expected = "unordered list"
        self.assertEqual(expected, block_to_block_type(markdown))

    def test_ordered(self):
        markdown = "1. this is\n2. an unordered\n3. list"
        expected = "ordered list"
        self.assertEqual(expected, block_to_block_type(markdown))


if __name__ == "__main__":
    unittest.main()
