import locale
from typing import Tuple, Optional

DECODING_ORDER = [
    "windows-1250",
    "windows-1251",
    "windows-1252",
    "windows-1253",
    "windows-1254",
    "utf-8",
]
SYMBOLS_WHEN_ENCODING_UTF8_AS_WIN1250 = [
    "Ĺş",
    "ĹĽ",
    "Ĺ‚",
    "Ĺ›",
    "Ä‡",
    "Ä…",
    "Ä™",
    "Ăł",
    "Ĺ„",
]
POLISH_DIACRITICS = ["ź", "ż", "ł", "ś", "ć", "ą", "ę", "ó", "ń"]
CHECK_IN_WORD_COUNT = 1000


def _diacritics_count_in_word(word: str) -> int:
    return len([pd for pd in POLISH_DIACRITICS if pd.lower() in word.lower()])


def _err_symbol_count_in_word(word: str) -> int:
    return len([err_sym for err_sym in SYMBOLS_WHEN_ENCODING_UTF8_AS_WIN1250 if err_sym.lower() in word.lower()])


def _is_correct_encoding(subs: str) -> bool:
    err_symbols, diacritics = 0, 0
    for word in subs.split()[:CHECK_IN_WORD_COUNT]:
        diacritics += _diacritics_count_in_word(word)
        err_symbols += _err_symbol_count_in_word(word)
    return err_symbols < diacritics


def _try_decode(subs: bytes) -> Tuple[str, str]:
    last_exc = None
    for i, enc in enumerate(DECODING_ORDER):
        try:
            encoded_subs = subs.decode(enc)
            if _is_correct_encoding(encoded_subs):
                return enc, encoded_subs
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
