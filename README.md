# napi.py
Unix CLI script for downloading subtitles from napiprojekt.pl

## installation
- prerequisites:
    - Python 3.6 or newer
    - `7z` available on PATH
- clone repository, enter `napi.py` directory and run:
    - `sudo pip install .` for system wide installation

## usage
- execute in shell `napi-py MyMovie.mkv`

## development
- `make config` installs `venv` under `.venv/napi.py`
- `make build` creates installable packages
- `make test` runs unit tests