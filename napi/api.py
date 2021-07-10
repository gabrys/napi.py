import os
from urllib import request


def _cipher(z):
    idx = [0xE, 0x3, 0x6, 0x8, 0x2]
    mul = [2, 2, 5, 4, 3]
    add = [0, 0xD, 0x10, 0xB, 0x5]

    b = []
    for i in range(len(idx)):
        a = add[i]
        m = mul[i]
        i = idx[i]

        t = a + int(z[i], 16)
        v = int(z[t : t + 2], 16)
        b.append(("%x" % (v * m))[-1])

    return "".join(b)


def _build_url(movie_hash):
    return "http://napiprojekt.pl/unit_napisy/dl.php?l=PL&f={}&t={}&v=other&kolejka=false&nick=&pass=&napios={}".format(
        movie_hash, _cipher(movie_hash), os.name
    )


def download_for(movie_hash: str) -> bytes:
    the_url = _build_url(movie_hash)
    return request.urlopen(the_url).read()
