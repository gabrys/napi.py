import argparse
import logging
import time
import traceback
from os import path
from typing import Optional

from napi import NapiPy
from napi.store_subs import get_target_path_for_subtitle

EXIT_CODE_OK = 0
EXIT_CODE_WRONG_ARGS = 1
EXIT_CODE_NO_SUCH_MOVIE = 2
EXIT_SUBS_NOT_FOUND = 4
EXIT_CODE_FAILED = 5


def setup_logger(level: int = logging.INFO) -> None:
    logging.basicConfig(format="%(asctime)s UTC | %(levelname)s | %(message)s", level=level)
    logging.Formatter.converter = time.gmtime


class NoMatchingSubtitle(Exception):
    pass


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="napi-py", description="CLI for downloading subtitles from napiprojekt.pl")
    parser.add_argument("movie_path", type=str, help="Path to movie file")
    parser.add_argument(
        "--target",
        type=str,
        required=False,
        default=None,
        help="Path to store the subtitles in",
    )
    parser.add_argument(
        "--hash",
        type=str,
        required=False,
        default=None,
        help="Use given hash for this movie",
    )
    parser.add_argument(
        "--from-enc",
        type=str,
        required=False,
        default=None,
        help="Treat downloaded subs as this encoding instead of guessing",
    )
    return parser.parse_args()


def main(
    movie_path: str,
    subtitles_path: Optional[str] = None,
    use_hash: Optional[str] = None,
    from_enc: Optional[str] = None,
) -> None:
    log = logging.getLogger()
    movie_path = path.abspath(movie_path)
    subtitles_path = path.abspath(subtitles_path or get_target_path_for_subtitle(movie_path))
    if path.exists(movie_path):
        if use_hash and use_hash.startswith("napiprojekt:"):
            use_hash = use_hash.partition("napiprojekt:")[-1]
        try:
            napi_client = NapiPy()
            movie_hash = use_hash or napi_client.calc_hash(movie_path)
            log.info("Downloading subs for {} (hash: {})".format(path.basename(movie_path), movie_hash))
            src_enc, tgt_src, tmp_file = napi_client.download_subs(movie_hash, use_enc=from_enc)
            if src_enc is not None and tmp_file is not None:
                subs_path = (
                    napi_client.move_subs(tmp_file, subtitles_path)
                    if subtitles_path
                    else napi_client.move_subs_to_movie(tmp_file, movie_path)
                )
                log.info("Saved subs ({} -> {}) in {}".format(src_enc, tgt_src, subs_path))
            else:
                log.error("Napiprojekt.pl does not have subtitles for this movie")
                exit(EXIT_SUBS_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            log.error(e)
            exit(EXIT_CODE_FAILED)
    else:
        log.error("No such file: {}".format(movie_path))
        exit(EXIT_CODE_NO_SUCH_MOVIE)


def cli_main():
    setup_logger()
    log = logging.getLogger()
    try:
        args = _parse_args()
        main(
            args.movie_path,
            subtitles_path=args.target,
            use_hash=args.hash,
            from_enc=args.from_enc,
        )
    except Exception as e:
        log.error("Parameters error: {}".format(e))
        exit(EXIT_CODE_WRONG_ARGS)
    exit(EXIT_CODE_OK)
