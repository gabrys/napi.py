#!/usr/bin/python3

#
# Script downloads subtitles from napiprojekt
#
# based on older script
# by gim,krzynio,dosiu,hash 2oo8.
# last modified: 2018-08-12
# 4pc0h f0rc3

import sys
from urllib import request
import os
import hashlib

from tempfile import NamedTemporaryFile
from subprocess import Popen, PIPE

EXIT_CODE_WRONG_ARG_NUMBER = 1
EXIT_CODE_LACK_OF_7Z_ON_PATH = 4
EXIT_CODE_FAILED = 8

TMP_FILE_SUFFIX = ".7z"
TMP_FILE_PREFIX = "un7zip"
SIZE_10_MBs_IN_BYTES = 10485760
NAPI_ARCHIVE_PASSWORD = "iBlm8NTigvru0Jr0"


class Un7ZipError(Exception):
    pass


class NoMatchingSubtitle(Exception):
    pass


def f(z):
    idx = [0xe, 0x3, 0x6, 0x8, 0x2]
    mul = [2, 2, 5, 4, 3]
    add = [0, 0xd, 0x10, 0xb, 0x5]

    b = []
    for i in range(len(idx)):
        a = add[i]
        m = mul[i]
        i = idx[i]

        t = a + int(z[i], 16)
        v = int(z[t:t + 2], 16)
        b.append(("%x" % (v * m))[-1])

    return "".join(b)


def build_url(movie_hash):
    return "http://napiprojekt.pl/unit_napisy/dl.php?l=PL&f={}&t={}&v=other&kolejka=false&nick=&pass=&napios={}".format(
        movie_hash, f(movie_hash), os.name)


def calc_movie_hash_as_hex(movie_path):
    md5_hash_gen = hashlib.md5()
    with open(movie_path, mode='rb') as movie_file:
        content_of_first_10mbs = movie_file.read(SIZE_10_MBs_IN_BYTES)
    md5_hash_gen.update(content_of_first_10mbs)
    return md5_hash_gen.hexdigest()


def un7zip(archive, password=None):
    tmp_file = NamedTemporaryFile(prefix=TMP_FILE_PREFIX, suffix=TMP_FILE_SUFFIX)
    tmp_file.write(archive)
    tmp_file.flush()

    cmd = ["7z", "x", "-y", "-so"]
    if password is not None:
        cmd += ["-p" + password]
    cmd += [tmp_file.name]

    sp = Popen(cmd, stdout=PIPE, stderr=PIPE)

    content = sp.communicate()[0]

    if sp.wait() != 0:
        raise Un7ZipError("Downloaded archive with subtitles is broken!")

    tmp_file.close()  # deletes the file
    return content


def get_target_path_for_subtitle(movie_path):
    filename, extension = os.path.splitext(movie_path)
    return filename + ".txt"


def un7zip_api_response(content_7z: bytes) -> bytes:
    try:
        content = un7zip(content_7z, password=NAPI_ARCHIVE_PASSWORD)
    except Un7ZipError:
        raise NoMatchingSubtitle("No matching subtitle")
    return content


def download_subtitle(movie_path):
    movie_hash = calc_movie_hash_as_hex(movie_path)
    napi_subs_dl_url = build_url(movie_hash)
    content_7z = request.urlopen(napi_subs_dl_url).read()
    binary_content = un7zip_api_response(content_7z)
    encoded_content = encode_to_unicode(binary_content)
    with open(get_target_path_for_subtitle(movie_path), "w") as subtitles_file:
        subtitles_file.write(encoded_content)


def encode_to_unicode(binary_content: bytes) -> str:
    return binary_content.decode("windows-1250")


def main(args):
    if len(args) < 1:
        print("\nUSAGE:\n\tnapiprojekt.py moviefile [moviefile, ...]\n\n")
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

