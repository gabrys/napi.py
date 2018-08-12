### napi.py
CLI script to download subtitles from napiprojekt.pl

#### Requirements
- Python 3
- 7-zip (7z available on PATH)
- Internet connection

#### Usage
- execute in Terminal `napiprojekt.py /path/to/movie` 
- or `napiprojekt.py /path/to/movie1 /path/to/movie2` for multiple movies
- subtitles shall be downloaded to the directory with movie, with `.txt` extension 

#### Notices
- implemented encoding from `windows-1250` to unicode correctly, so english Windows and Linux should display diacritics (ś, ę, ł, ó etc.) in subtitles correctly