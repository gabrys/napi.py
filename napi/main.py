#!/usr/bin/python3

import os
import sys

from napi.api import build_url, download
from napi.hash import calc_movie_hash_as_hex
from napi.read_7z import un7zip_api_response

EXIT_CODE_WRONG_ARG_NUMBER = 1
EXIT_CODE_LACK_OF_7Z_ON_PATH = 4
EXIT_CODE_FAILED = 8


class NoMatchingSubtitle(Exception):
    pass


def get_target_path_for_subtitle(movie_path):
    filename, extension = os.path.splitext(movie_path)
    return filename + ".txt"


def download_subtitle(movie_path):
    movie_hash = calc_movie_hash_as_hex(movie_path)
    napi_subs_dl_url = build_url(movie_hash)
    content_7z = download(napi_subs_dl_url)
    binary_content = un7zip_api_response(content_7z)
    encoded_content = encode_to_unicode(binary_content)
    with open(get_target_path_for_subtitle(movie_path), "w") as subtitles_file:
        subtitles_file.write(encoded_content)


def encode_to_unicode(binary_content: bytes) -> str:
    return binary_content.decode("windows-1250")


def main(args):
    if len(args) < 1:
        print("\nUSAGE:\n\tmain.py moviefile [moviefile, ...]\n\n")
        exit(EXIT_CODE_WRONG_ARG_NUMBER)

    any_failure = False
    try:
        for index, movie_path in enumerate(args):
            print("{}/{} | Downloading subtitles for {} ...".format(index + 1, len(args), movie_path))
            try:
                download_subtitle(movie_path)
                print("{}/{} | Success!".format(index + 1, len(args)))
            except NoMatchingSubtitle:
                any_failure = True
                print("{}/{} | No subtitles found!".format(index + 1, len(args)))
            except IOError as e:
                print("{}/{} | Cannot read movie file: {}".format(index + 1, len(args), e))
    except OSError:
        print("OS error. Is 7z in PATH?")
        exit(EXIT_CODE_LACK_OF_7Z_ON_PATH)
    if any_failure:
        exit(EXIT_CODE_FAILED)


if __name__ == "__main__":
    program_args = sys.argv[1:]
    main(program_args)
