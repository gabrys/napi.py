import os
import unittest

from napi.main import build_url, un7zip_api_response, encode_to_unicode

COMPRESSED_SUBTITLES_FILE_NAME = 'DunkirkSubtitles.7zip'


class NapiPyTest(unittest.TestCase):
    def test_should_generate_correct_url(self):
        movie_hash = '6e7d92a7c0f40706067248d50d3b1d5a'
        expected_url = 'http://napiprojekt.pl/unit_napisy/dl.php?l=PL&f=6e7d92a7c0f40706067248d50d3b1d5a&t=c6705&v=other&kolejka=false&nick=&pass=&napios={}'.format(
            os.name)
        actual_url = build_url(movie_hash)
        self.assertEqual(expected_url, actual_url)

    def test_should_unpack_downloaded_7zip(self):
        with open(COMPRESSED_SUBTITLES_FILE_NAME, 'rb') as input_file:
            compressed_content = input_file.read()
        sub_bin_content = un7zip_api_response(compressed_content)
        expected_phrase = b"GrupaHatak.pl"
        self.assertIn(expected_phrase, sub_bin_content)

    def test_should_encode_subtitles_correctly(self):
        with open(COMPRESSED_SUBTITLES_FILE_NAME, 'rb') as input_file:
            compressed_content = input_file.read()
        sub_bin_content = un7zip_api_response(compressed_content)
        sub_utf8_content = encode_to_unicode(sub_bin_content)
        expected_phrases = ['Tłumaczenie', 'Dunkierką', 'Francuzów', 'Uwięzieni']
        for expected_phrase in expected_phrases:
            self.assertIn(expected_phrase, sub_utf8_content)
