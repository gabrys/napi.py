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

SIZE_10_MBs_IN_BYTES = 10485760
NAPI_ARCHIVE_PASSWORD = "iBlm8NTigvru0Jr0"


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


def build_url(movie_path):
    movie_hash = calc_movie_hash_as_hex(movie_path)
    url = "http://napiprojekt.pl/unit_napisy/dl.php?l=PL&f={}&t={}&v=other&kolejka=false&nick=&pass=&napios={}".format(
        movie_hash, f(movie_hash), os.name)
    return url


def calc_movie_hash_as_hex(movie_path):
    md5_hash_gen = hashlib.md5()
    md5_hash_gen.update(open(movie_path, mode='rb').read(SIZE_10_MBs_IN_BYTES))
    return md5_hash_gen.hexdigest()


class Un7ZipError(Exception):
    pass


def un7zip(archive, password=None, tmp_file_prefix="un7zip", tmp_file_suffix=".7z"):
    tmp_file = NamedTemporaryFile(prefix=tmp_file_prefix, suffix=tmp_file_suffix)
    tmp_file.write(archive)
    tmp_file.flush()

    cmd = ["7z", "x", "-y", "-so"]
    if password is not None:
        cmd += ["-p" + password]
    cmd += [tmp_file.name]

    sp = Popen(cmd, stdout=PIPE, stderr=PIPE)

    content = sp.communicate()[0]

    if sp.wait() != 0:
        raise Un7ZipError("Invalid archive")

    tmp_file.close()  # deletes the file
    return content


def get_path_for_subtitle(movie_path):
    filename, extension = os.path.splitext(movie_path)
    return filename + ".txt"


class NoMatchingSubtitle(Exception):
    pass


def download_subtitle(movie_path):
    napi_url = build_url(movie_path)
    content_7z = request.urlopen(napi_url).read()
    try:
        content = un7zip(content_7z, password=NAPI_ARCHIVE_PASSWORD)
    except Un7ZipError:
        raise NoMatchingSubtitle("No matching subtitle")

    # Don't override the same subtitles
    try:
        same = open(get_path_for_subtitle(movie_path), "rb").read() == content
    except IOError:
        same = False

    if not same:
        open(get_path_for_subtitle(movie_path), "wb").write(content)


def main():
    if len(sys.argv) < 2:
        print("\nUSAGE:\n\t" + sys.argv[0] + " moviefile [moviefile, ...]\n\n")
        exit(1)

    failed = False
    try:
        for movie_path in sys.argv[1:]:
            try:
                download_subtitle(movie_path)
                print("OK " + movie_path)
            except NoMatchingSubtitle:
                failed = True
                print("No subtitles for: " + movie_path)
            except IOError:
                print("Cannot read file " + movie_path + "\n")
                exit(2)
    except OSError:
        print("OS error. Is 7z in PATH?")
        exit(4)

    if failed:
        exit(8)


if __name__ == "__main__":
    main()
