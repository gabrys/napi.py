import os


def get_target_path_for_subtitle(movie_path: str) -> str:
    filename, extension = os.path.splitext(movie_path)
    return filename + ".srt"


def store_subtitles(subtitles_path: str, binary_subs: bytes) -> str:
    with open(subtitles_path, "wb") as subtitles_file:
        subtitles_file.write(binary_subs)
    return subtitles_path
