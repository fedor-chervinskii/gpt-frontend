from unittest import TestCase
from gpt_frontend.summarize import text_block_iterator


class TestText_block_iterator(TestCase):
    def test_text_block_iterator(self):
        text = "one two three four, five six seven eight nine ten eleven"
        for block in text_block_iterator(text, max_words=3):
            self.assertLessEqual(len(block.split()), 3)

        self.assertEqual(list(text_block_iterator(text, max_words=12))[0], text)

        self.assertEqual(len(list(text_block_iterator(text, max_words=8))), 2)
