import os


def _get_target_path_for_subtitle(movie_path: str) -> str:
    filename, extension = os.path.splitext(movie_path)
    return filename + ".txt"


def store_subtitles(binary_subs: bytes, movie_path: str) -> str:
    store_path = _get_target_path_for_subtitle(movie_path)
    with open(store_path, "wb") as subtitles_file:
        subtitles_file.write(binary_subs)
    return store_path
