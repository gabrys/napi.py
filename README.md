# napi.py
Unix CLI script for downloading subtitles from napiprojekt.pl

## Installation
- prerequisites: `python3` and `7z` available on PATH
- `pip install napi-py`

## Usage
- execute in Terminal `napi-py MyMovie.mkv` (or `napi-py MyMovie1.mkv MyMovie2.mkv` for multiple movies)

## Notices
- implemented encoding from `windows-1250` to unicode correctly, so english Windows and Linux should display diacritics (ś, ę, ł, ó etc.) in subtitles correctly