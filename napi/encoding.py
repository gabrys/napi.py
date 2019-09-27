import locale
from typing import Tuple, Optional

DECODING_ORDER = ["windows-1250", "windows-1251", "windows-1252", "windows-1253", "windows-1254", "utf-8"]


def _try_decode(subs: bytes) -> Tuple[str, str]:
    last_exc = None
    for i, enc in enumerate(DECODING_ORDER):
        try:
            return enc, subs.decode(enc)
        except UnicodeDecodeError as e:
            last_exc = e
    raise ValueError("Could not encode using any of {}: {}".format(DECODING_ORDER, last_exc))


def decode_subs(subtitles_binary: bytes, use_enc: Optional[str] = None) -> Tuple[str, str]:
    if use_enc is not None:
        return use_enc, subtitles_binary.decode(use_enc)
    else:
        return _try_decode(subtitles_binary)


def encode_subs(subs: str) -> Tuple[str, bytes]:
    target_encoding = locale.getpreferredencoding()
    return target_encoding, subs.encode(target_encoding)
