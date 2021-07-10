import os
import shutil
import tempfile
from typing import Tuple, Optional

from napi.api import download_for
from napi.encoding import decode_subs, encode_subs
from napi.hash import calc_movie_hash_as_hex
from napi.read_7z import un7zip_api_response
from napi.store_subs import get_target_path_for_subtitle


class NapiPy:
    def __init__(self) -> None:
        pass

    def calc_hash(self, movie: str) -> str:
        return calc_movie_hash_as_hex(movie)

    def download_subs(
        self, movie_hash: str, use_enc: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        subs_bin = un7zip_api_response(download_for(movie_hash))
        if subs_bin:
            src_enc, subs_utf8 = decode_subs(subs_bin, use_enc=use_enc)
            tgt_enc, subs_bin = encode_subs(subs_utf8)
            with tempfile.NamedTemporaryFile(delete=False) as fileTemp:
                fileTemp.write(subs_bin)
            return src_enc, tgt_enc, fileTemp.name
        return None, None, None

    def move_subs_to_movie(self, tmp_subs: str, movie: str) -> str:
        tgt_path = get_target_path_for_subtitle(movie)
        shutil.copy(tmp_subs, tgt_path)
        os.remove(tmp_subs)
        return tgt_path

    def move_subs(self, tmp_subs: str, path: str) -> str:
        shutil.copy(tmp_subs, path)
        os.remove(tmp_subs)
        return path
