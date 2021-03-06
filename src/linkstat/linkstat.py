#! /usr/bin/python3

import re

from . import __version__, Actions, Stat



def getOptions():
    from argparse import ArgumentParser

    prs = ArgumentParser(
        description="Compare folders and report on hard links",
        epilog="""WARNING : Both folders must be in the same file system.
                  Providing a folder twice will produce all duplicates.""",
        )

    prs.add_argument(
        "-v", "--version",
        action="version",
        version=__version__
        )

    grp = prs.add_argument_group("Comparison action")
    actions = grp.add_mutually_exclusive_group(required=True)
    actions.add_argument(
        "-o", "--or",
        help="Report inodes found in any of the folders",
        action="store_const",
        dest="action",
        const=Actions.OR,
        )
    actions.add_argument(
        "-a", "--and",
        help="Report inodes found in every folder",
        action="store_const",
        dest="action",
        const=Actions.AND,
        )
    actions.add_argument(
        "-u", "--unique",
        help="Report inodes found in only one of the folders",
        action="store_const",
        dest="action",
        const=Actions.UNIQUE,
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
    ops.FOLDERS.append(ops.FOLDER)

    ops.exclude = [re.compile(r) for r in ops.exclude]

    return ops



def main():
    ops = getOptions()
    linkStat = Stat(ops.FOLDERS, ops.exclude)
    rv = linkStat.run(ops.action)

    for files in linkStat.result.values():
        for f in files:
            print(f)

    if linkStat.result:
        exit(0)
    else:
        exit(1)



if __name__ == "__main__": main()
