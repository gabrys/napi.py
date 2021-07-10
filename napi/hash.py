import hashlib

SIZE_10_MBs_IN_BYTES = 10485760


def calc_movie_hash_as_hex(movie_path: str) -> str:
    md5_hash_gen = hashlib.md5()
    with open(movie_path, mode="rb") as movie_file:
        content_of_first_10mbs = movie_file.read(SIZE_10_MBs_IN_BYTES)
    md5_hash_gen.update(content_of_first_10mbs)
    return md5_hash_gen.hexdigest()
