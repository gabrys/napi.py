import argparse
import shutil
import traceback
from os import path
from typing import Optional

from napi.api import download_for
from napi.encoding import convert_subtitles_encoding
from napi.hash import calc_movie_hash_as_hex
from napi.read_7z import un7zip_api_response
from napi.store_subs import store_subtitles, get_target_path_for_subtitle

EXIT_CODE_OK = 0
EXIT_CODE_WRONG_ARGS = 1
EXIT_CODE_NO_SUCH_MOVIE = 2
EXIT_CODE_LACK_OF_7Z_ON_PATH = 3
EXIT_CODE_FAILED = 4


class NoMatchingSubtitle(Exception):
    pass


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="napi-py", description='CLI for downloading subtitles from napiprojekt.pl')
    parser.add_argument('movie_path', type=str, help='Path to movie file')
    parser.add_argument('--target', type=str, required=False, default=None, help='Path to store the subtitles in')
    return parser.parse_args()


def _is_7z_on_path(command: str = "7z") -> bool:
    return shutil.which(command) is not None


def main(movie_path: str, subtitles_path: Optional[str] = None) -> None:
    movie_path = path.abspath(movie_path)
    subtitles_path = path.abspath(subtitles_path or get_target_path_for_subtitle(movie_path))
    if path.exists(movie_path):
        if _is_7z_on_path():
            try:
                movie_hash = calc_movie_hash_as_hex(movie_path)
                print("Downloading for {} ({})".format(path.basename(movie_path), movie_hash))
                content_7z = download_for(movie_hash)
                subtitles_as_bytes = un7zip_api_response(content_7z)
                src_enc, tgt_enc, subtitles_as_target_bytes = convert_subtitles_encoding(subtitles_as_bytes)
                subtitles_path = store_subtitles(subtitles_path, subtitles_as_target_bytes)
                print("Saved subs ({} -> {}) in {}".format(src_enc, tgt_enc, subtitles_path))
            except Exception as e:
                traceback.print_exc()
                print("Error: ".format(e))
                exit(EXIT_CODE_FAILED)
        else:
            print("Error: 7z seems to be unavailable on PATH!")
            exit(EXIT_CODE_LACK_OF_7Z_ON_PATH)
    else:
        print("Error: no such file: {}".format(movie_path))
        exit(EXIT_CODE_NO_SUCH_MOVIE)


def cli_main():
    try:
        args = _parse_args()
        main(args.movie_path)
    except Exception as e:
        print("Parameters error: {}".format(e))
        exit(EXIT_CODE_WRONG_ARGS)
    exit(EXIT_CODE_OK)
