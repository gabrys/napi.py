from distutils.core import setup
from setuptools import find_packages

REQUIREMENTS = [
]

REQUIREMENTS_DEV = [
    "mypy>=0.660,<1.0.0",
    "pytest>=4.1.1,<5.0.0",
    "wheel>=0.32.3,<1.0.0"
]

setup(
    name="napi-py",
    version="0.1.1",
    description="CLI for downloading subtitles from napiprojekt.pl",
    author="Mateusz Korzeniowski",
    author_email="emkor93@gmail.com",
    url="https://github.com/emkor/napi.py",
    packages=find_packages(exclude=("test", "test.*")),
    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS_DEV,
    extras_require={
        "dev": REQUIREMENTS_DEV
    },
    entry_points={
        "console_scripts": [
            "napi-py = napi.main:cli_main"
        ]
    }
)
