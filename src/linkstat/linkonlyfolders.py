#! /usr/bin/python3

import re

from . import __version__, Actions, Stat



def getOptions():
    from argparse import ArgumentParser

    prs = ArgumentParser(
        description="List folders that include only links to files found in previous folders.",
        epilog="""WARNING : All folders must be in the same file system. Folders are compared with their predecessor, in the given order.""",
        )

    prs.add_argument(
        "-v", "--version",
        action="version",
        version=__version__
        )

    prs.add_argument(
        "-x", "--exclude",
        help="Exclude files whose name match the given regex",
        action="append",
        default=[],
        )

    prs.add_argument(
        "FOLDER",
        help="Folder to search for links",
        )

    prs.add_argument(
        "FOLDERS",
        nargs="+",
        metavar="FOLDER",
        )

    ops = prs.parse_args()
    ops.FOLDERS.insert(0, ops.FOLDER)

    ops.exclude = [re.compile(r) for r in ops.exclude]

    return ops



def getNonUniques(folders, exclude):
    last = folders.pop(0)
    for f in folders:
        linkStat = Stat((last, f), exclude)
        linkStat.run(Actions.UNIQUE)
        if not linkStat.result:
            yield f
        else:
            last = f



def main():
    ops = getOptions()
    for fp in getNonUniques(ops.FOLDERS, ops.exclude):
        print(fp)



if __name__ == "__main__": main()
