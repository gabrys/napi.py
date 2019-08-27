from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
from typing import Optional

TMP_FILE_SUFFIX = ".7z"
TMP_FILE_PREFIX = "un7zip"
NAPI_ARCHIVE_PASSWORD = "iBlm8NTigvru0Jr0"


class Un7ZipError(Exception):
    pass


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


def un7zip_api_response(content_7z: bytes) -> Optional[bytes]:
    try:
        return un7zip(content_7z, password=NAPI_ARCHIVE_PASSWORD)
    except Un7ZipError:
        return None
