#! /usr/bin/env python3

from liblinkstat import __version__
from setuptools import setup



setup(
    name='linkstat',
    version=__version__,
    description='Scipts to work with hard linked folder copies',
    url='https://github.com/francoistrahan/linkstat',

    author='François Trahan',
    author_email='francois.trahan@gmail.com',

    packages=[
        "linkstat",
        ],

    entry_points={
        'console_scripts': [
            'linkstat = linkstat.linkstat:main',
            'listonce = linkstat.listonce:main',
            'linkonlyfolders = linkstat.linkonlyfolders:main',
            'stat = linkstat.stat:main',
            ],
        },

    )
