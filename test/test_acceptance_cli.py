from os import path
import subprocess
import tempfile


def test_should_physically_download_subtitle_file():
    with tempfile.NamedTemporaryFile() as _movie_file:
        cmd = f'napi-py --from-enc utf-8 --hash 25b1087d997bfbf8a4be462255e05a05 {_movie_file.name}'
        subprocess.check_call(cmd.split())
        expected_subs_file = f'{_movie_file.name}.srt'
        assert path.isfile(expected_subs_file), f'Expected subtitles file under {expected_subs_file} is absent'

        with open(expected_subs_file, 'rt') as _sub_file:
            subs = _sub_file.readlines()
        first_20_subs = [l.strip().lower() for l in subs[:20]]
        expected_sub_phrase = 'ŻOŁNIERZE KOSMOSU'
        assert expected_sub_phrase.strip().lower() in first_20_subs, \
            f"{expected_sub_phrase} not found in first 20 lines of file {expected_subs_file}"
