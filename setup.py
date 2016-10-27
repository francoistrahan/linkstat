#! /usr/bin/env python3

from os import umask
from liblinkstat import __version__
from distutils.core import setup

umask(0o022)

setup(
    name='linkstat',
    version=__version__,
    description='Scipts to work with hard linked folder copies',
    author='François Trahan',
    author_email='francois.trahan@gmail.com',
    url='https://rm.ftrahan.com/projects/linkstat',
    packages=[
        "liblinkstat",
        ],
    scripts=[
        "linkonlyfolders",
        "linkstat",
        "listonce",
        ],
#    data_files=[
#        (
#            "share/libftbackup/samples",
#            [
#                "samples/exclude.regex",
#                "samples/nocompress.regex",
#                "samples/prune.regex",
#                "samples/wraperscript",
#                ]),
#        ],
    )
