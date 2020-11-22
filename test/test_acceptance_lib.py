import unittest

from napi import NapiPy


class NapiPyAcceptanceTest(unittest.TestCase):
    def test_should_download_correctly_encoded_subs(self):
        movie_hash = '25b1087d997bfbf8a4be462255e05a05'
        napi = NapiPy()
        src_enc, tgt_enc, tmp_file = napi.download_subs(movie_hash)
        self.assertEqual(src_enc, "utf-8")

        with open(tmp_file) as subs_file:
            subs = subs_file.read()

        expected_phrases = ['źródło', 'władzę', 'Dziękuję', 'zgłębiają', 'ZWYCIĘŻĄ!']
        for expected_phrase in expected_phrases:
            self.assertIn(expected_phrase, subs)

    def test_should_return_none_when_no_subtitles_for_movie(self):
        movie_hash = '00000000000000000000000000000000'
        napi = NapiPy()
        src_enc, tgt_enc, tmp_file = napi.download_subs(movie_hash)
        self.assertIsNone(src_enc)
        self.assertIsNone(tmp_file)

    def test_should_download_subs_with_forced_encoding(self):
        movie_hash = '0e9b0d0d3dc5abc0538d207d477af4a1'
        napi = NapiPy()
        src_enc, tgt_enc, tmp_file = napi.download_subs(movie_hash, use_enc="utf-8")
        self.assertEqual(src_enc, "utf-8")

        with open(tmp_file) as subs_file:
            subs = subs_file.read()

        expected_phrases = ['ciąży', 'artykułów', 'Właśnie', 'wyjść', 'wciąż']
        for expected_phrase in expected_phrases:
            self.assertIn(expected_phrase, subs)
