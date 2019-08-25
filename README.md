# napi.py [![Build Status](https://travis-ci.com/emkor/napi.py.svg?branch=master)](https://travis-ci.com/emkor/napi.py)
Unix CLI script for downloading subtitles from napiprojekt.pl

## installation
- prerequisites:
    - Python 3.6 or newer
    - `7z` available on PATH
- clone repository, enter `napi.py` directory and run:
    - `sudo pip install .` for system wide installation

## usage as tool
- execute in shell `napi-py MyMovie.mkv`

## usage as lib
```python
from napi import NapiPy

movie_path = "~/Downloads/MyMovie.mp4"

napi = NapiPy()
movie_hash = napi.calc_hash(movie_path)
source_encoding, tmp_file = napi.download_subs(movie_hash)
subs_path = napi.move_subs_to_movie(tmp_file, movie_path)
print(subs_path)
```

## development
- `make config` installs `venv` under `.venv/napi.py`
- `make build` creates installable packages
- `make test` runs unit and acceptance tests