from os import path
import subprocess
import tempfile
from typing import List


def _read_first_lines_of_subs(subs_file: str, lines: int = 20) -> List[str]:
    with open(subs_file, 'rt') as _sub_file:
        subs = _sub_file.readlines()
    return [l.strip() for l in subs[:lines]]


def _contains_phrase(phrase: str, text: List[str]) -> bool:
    phrase = phrase.strip().lower()
    return any([phrase in line.strip().lower() for line in text])


def test_should_physically_download_subtitle_file():
    with tempfile.NamedTemporaryFile() as _movie_file:
        cmd = f'napi-py --from-enc utf-8 --hash 25b1087d997bfbf8a4be462255e05a05 {_movie_file.name}'
        subprocess.run(cmd.split(), timeout=10.)
        expected_subs_file = f'{_movie_file.name}.srt'
        assert path.isfile(expected_subs_file), f'Expected subtitles file under {expected_subs_file} is absent'

        first_20_lines = _read_first_lines_of_subs(expected_subs_file, 20)
        expected_phrase = 'ŻOŁNIERZE KOSMOSU'
        assert _contains_phrase(expected_phrase, first_20_lines), \
            f"{expected_phrase} not found in first 20 lines of file {expected_subs_file}"


def test_should_download_and_correctly_encode_utf8_src_subs():
    with tempfile.NamedTemporaryFile() as _movie_file:
        cmd = f'napi-py --from-enc utf-8 --hash 0e9b0d0d3dc5abc0538d207d477af4a1 {_movie_file.name}'
        subprocess.run(cmd.split(), timeout=10.)
        expected_subs_file = f'{_movie_file.name}.srt'
        assert path.isfile(expected_subs_file), f'Expected subtitles file under {expected_subs_file} is absent'

        first_20_lines = _read_first_lines_of_subs(expected_subs_file, 20)
        expected_phrase = 'rządzie ciąży'
        assert _contains_phrase(expected_phrase, first_20_lines), \
            f"{expected_phrase} not found in first 20 lines of file {expected_subs_file}"
