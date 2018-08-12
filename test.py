import os
import unittest

from napiprojekt import build_url, un7zip_api_response


class NapiPyTest(unittest.TestCase):
    def test_should_generate_correct_url(self):
        movie_hash = '6e7d92a7c0f40706067248d50d3b1d5a'
        expected_url = 'http://napiprojekt.pl/unit_napisy/dl.php?l=PL&f=6e7d92a7c0f40706067248d50d3b1d5a&t=c6705&v=other&kolejka=false&nick=&pass=&napios={}'.format(
            os.name)
        actual_url = build_url(movie_hash)
        self.assertEqual(expected_url, actual_url)

    def test_should_unpack_downloaded_7zip(self):
        compressed_subtitles_file_name = 'DunkirkSubtitles.7zip'
        with open(compressed_subtitles_file_name, 'rb') as input_file:
            compressed_content = input_file.read()
        content = un7zip_api_response(compressed_content)
        self.assertIn(b"GrupaHatak.pl", content)
        print(content)
