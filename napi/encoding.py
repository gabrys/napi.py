import locale
from typing import Tuple

DECODING_ORDER = ["windows-1250", "windows-1251", "windows-1252", "windows-1253", "windows-1254", "utf-8"]


def _try_decode(binary: bytes) -> Tuple[str, str]:
    for i, enc in enumerate(DECODING_ORDER):
        try:
            text = binary.decode(enc)
            return enc, text
        except UnicodeDecodeError as e:
            if i == len(DECODING_ORDER) - 1:
                raise e
            else:
                pass


def convert_subtitles_encoding(subtitles_binary: bytes) -> Tuple[str, str, bytes]:
    target_encoding = locale.getpreferredencoding()
    source_encoding, subs = _try_decode(subtitles_binary)
    return source_encoding, target_encoding, subs.encode(target_encoding)
