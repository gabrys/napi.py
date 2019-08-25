import os
import unittest
from os import path

from napi.api import _build_url
from napi.encoding import decode_subs
from napi.read_7z import un7zip_api_response

TEST_SUBS_7Z = 'test/resources/DunkirkSubtitles.7zip'


def _get_project_dir(file_: str) -> str:
    curr_dir = os.path.dirname(os.path.realpath(file_))
    code_directory, proj_dir, _ = curr_dir.partition("napi.py")
    return path.join(code_directory, proj_dir)


class NapiPyTest(unittest.TestCase):
    def test_should_generate_correct_url(self):
        movie_hash = '6e7d92a7c0f40706067248d50d3b1d5a'
        expected_url = 'http://napiprojekt.pl/unit_napisy/dl.php?l=PL&f=6e7d92a7c0f40706067248d50d3b1d5a&t=c6705&v=other&kolejka=false&nick=&pass=&napios={}'.format(
            os.name)
        actual_url = _build_url(movie_hash)
        self.assertEqual(expected_url, actual_url)

    def test_should_unpack_downloaded_7zip(self):
        subs_path = path.join(_get_project_dir(__file__), TEST_SUBS_7Z)
        with open(subs_path, 'rb') as input_file:
            compressed_content = input_file.read()
        sub_bin_content = un7zip_api_response(compressed_content)
        expected_phrase = b"GrupaHatak.pl"
        self.assertIn(expected_phrase, sub_bin_content)

    def test_should_encode_subtitles_correctly(self):
        subs_path = path.join(_get_project_dir(__file__), TEST_SUBS_7Z)
        with open(subs_path, 'rb') as input_file:
            compressed_content = input_file.read()
        sub_bin_content = un7zip_api_response(compressed_content)
        _, sub_utf8_content = decode_subs(sub_bin_content)
        expected_phrases = ['Tłumaczenie', 'Dunkierką', 'Francuzów', 'Uwięzieni']
        for expected_phrase in expected_phrases:
            self.assertIn(expected_phrase, sub_utf8_content)
