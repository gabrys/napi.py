#!/usr/bin/python
#
# Script downloads subtitles from napiprojekt
#
# based on older script
# by gim,krzynio,dosiu,hash 2oo8.
# last modified: 6-I-2oo8
# 4pc0h f0rc3

import md5, sys, urllib, os

from tempfile import NamedTemporaryFile
from subprocess import Popen, PIPE


def f(z):
	idx = [ 0xe, 0x3,  0x6, 0x8, 0x2 ]
	mul = [   2,   2,    5,   4,   3 ]
	add = [   0, 0xd, 0x10, 0xb, 0x5 ]

	b = []
	for i in xrange(len(idx)):
		a = add[i]
		m = mul[i]
		i = idx[i]

		t = a + int(z[i], 16)
		v = int(z[t:t+2], 16)
		b.append( ("%x" % (v*m))[-1] )

	return "".join(b)


def napiurl(path):
    d = md5.new();
    d.update(open(path).read(10485760))
    h = d.hexdigest()

    return "http://napiprojekt.pl/unit_napisy/dl.php?l=PL&" + \
        "f=" + h + "&t=" + f(h) + \
        "&v=other&kolejka=false&nick=&pass=&napios=" + os.name


class Un7ZipError(Exception):
    pass


def un7zip(archive, password=None, tmpfileprefix="un7zip", tmpfilesuffix=".7z"):
    tmpfile = NamedTemporaryFile(prefix=tmpfileprefix, suffix=tmpfilesuffix)
    tmpfile.write(archive)
    tmpfile.flush()

    cmd = ["7z", "x", "-y", "-so"]
    if password is not None:
        cmd += ["-p" + password]
    cmd += [tmpfile.name]

    sp = Popen(cmd, stdout=PIPE, stderr=PIPE)
        
    content = sp.communicate()[0]

    if sp.wait() != 0:
        raise Un7ZipError("Invalid archive")

    tmpfile.close() # deletes the file
    return content


def subtitlepath(moviepath):
    filename, fileext = os.path.splitext(moviepath)
    return filename + ".txt"


class NoMatchingSubtitle(Exception):
    pass


def download_subtitle(filename):
    url = napiurl(filename)
    content_7z = urllib.urlopen(url).read()
    try:
        content = un7zip(content_7z, password="iBlm8NTigvru0Jr0")
    except Un7ZipError:
        raise NoMatchingSubtitle("No matching subtitle")

    # Don't override the same subtitles
    try:
        same = open(subtitlepath(filename), "r").read() == content
    except IOError:
        same = False

    if not same:
        open(subtitlepath(filename), "w").write(content)


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("\nUSAGE:\n\t" + sys.argv[0] + " moviefile [moviefile, ...]\n\n")
        exit(1)

    failed = False
    try:
        for arg in sys.argv[1:]:
            try:
                download_subtitle(arg)
                print "OK " + arg
            except NoMatchingSubtitle:
                failed = True
                print "NOSUBS " + arg
            except IOError:
                sys.stderr.write("Cannot read file " + arg + "\n")
                exit(2)
    except OSError:
        print "OS error. Is 7z in PATH?"
        exit(4)

    if failed:
        exit(8)


if __name__ == "__main__":
    main()
