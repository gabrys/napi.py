# napi.py [![Build Status](https://travis-ci.com/emkor/napi.py.svg?branch=master)](https://travis-ci.com/emkor/napi.py)
CLI tool for downloading subtitles from napiprojekt.pl, fork of [gabrys/napi.py](https://github.com/gabrys/napi.py)

## prerequisites
- Python 3.6 or 3.7
- `7z` available on PATH

## installation
- `sudo pip install napi-py` for system wide installation

## usage as tool
- `napi-py ~/Downloads/MyMovie.mp4`

## usage as lib
```python
from napi import NapiPy

movie_path = "~/Downloads/MyMovie.mp4"

napi = NapiPy()
movie_hash = napi.calc_hash(movie_path)
source_encoding, target_encoding, tmp_file = napi.download_subs(movie_hash)
subs_path = napi.move_subs_to_movie(tmp_file, movie_path)
print(subs_path)
```

## development
- `make config` installs `venv` under `.venv/napi.py`
- `make build` creates installable packages
- `make test` runs unit and acceptance tests