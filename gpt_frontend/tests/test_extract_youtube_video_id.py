from unittest import TestCase
from gpt_frontend.summarize import extract_youtube_video_id


class TestExtract_youtube_video_id(TestCase):
    def test_extract_youtube_video_id(self):
        self.assertEqual(
            extract_youtube_video_id("https://youtube.com/watch?v=Y4izGi2tie4&feature=share"),
            "Y4izGi2tie4"
        )
        self.assertEqual(
            extract_youtube_video_id("https://youtu.be/EDSaOHx6wPI"),
            "EDSaOHx6wPI"
        )
        self.assertEqual(
            extract_youtube_video_id("https://youtu.be/Y4izGi2tie4"),
            "Y4izGi2tie4"
        )
