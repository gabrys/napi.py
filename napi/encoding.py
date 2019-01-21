import locale
from typing import Optional

import chardet


def _guess_encoding(binary: bytes) -> Optional[str]:
    return chardet.detect(binary).get("encoding")


def convert_subtitles_encoding(subtitles_binary: bytes) -> bytes:
    source_encoding = _guess_encoding(subtitles_binary) or "windows-1250"
    target_encoding = locale.getpreferredencoding()
    return subtitles_binary.decode(source_encoding).encode(target_encoding)
