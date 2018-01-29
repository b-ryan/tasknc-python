#!/usr/bin/env python3
from setuptools import setup

setup(
    name="pytasknc",
    version="0.1.2",
    description="NCurses for TaskWarrior",
    author="Buck Ryan",
    url="https://github.com/b-ryan/tasknc-python",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    install_requires=[
        "PyYAML>3,<=4",
    ],
    entry_points="""
    [console_scripts]
    pytasknc=pytasknc:main
    """,
    packages=["pytasknc"],
)
