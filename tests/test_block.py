import unittest

from block import markdown_to_blocks


# markdown_to_blocks("")
class TestBlock(unittest.TestCase):
    def test_one_block(self):
        markdown = "only one block of text"
        self.assertEqual([markdown], markdown_to_blocks(markdown))

    def test_multiple_blocks(self):
        markdown = "block one\n\nblock two\nhas two lines\n\nblock three"
        expected = ["block one", "block two\nhas two lines", "block three"]
        self.assertEqual(expected, markdown_to_blocks(markdown))
