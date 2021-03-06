#! /usr/bin/python3

from os import stat
from os.path import isfile

from . import __version__, ReportException



class App:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


    def getOptions(self):
        from argparse import ArgumentParser

        parser = ArgumentParser(
            description="Read a file names from stdin and outputs only one (the first) name per inode",
            epilog="WARNING : Files must be on the same file system. Giving a non-existent file name will terminate listing.",
            )

        parser.add_argument(
            "-v", "--version",
            action="version",
            version=__version__
            )

        parser.add_argument(
            "-0", "--null",
            help="Expect and return a null separated list instead of one per line",
            action="store_true",
            default=False,
            )

        parser.add_argument(
            "-r", "--reverse",
            help="Reverse the default behaviour: skip the first name per inode and give subsequent names",
            action="store_true",
            default=False,
            )

        self.options = parser.parse_args()
        if self.options.null:
            self.enumerator = self.enumerateByNull
            self.terminator = "\0"
        else:
            self.enumerator = self.enumerateByLine
            self.terminator = "\n"

        self.reverse = self.options.reverse


    def enumerateByNull(self):
        fn = ""
        while True:
            c = self.source.read(1)
            if c == "":
                break
            elif c == "\0":
                yield fn
                fn = ""
            else:
                fn += c


    def enumerateByLine(self):
        for line in self.source:
            yield line[:-1]


    def enumerateUniques(self):
        inodes = set()
        for fn in self.enumerator():
            if not isfile(fn):
                raise ReportException(1, "Not a valid file : \"{}\"".format(fn))
            inode = stat(fn).st_ino
            if inode not in inodes:
                inodes.add(inode)
                if not self.reverse:
                    yield fn
            elif self.reverse:
                yield fn
                    


    def printLines(self):
        for fn in self.enumerateUniques():
            print(fn, file=self.destination, end=self.terminator)



def main():
    from sys import stdin, stdout

    try:
        app = App(stdin, stdout)
        app.getOptions()
        app.printLines()
    except ReportException as e:
        print(e)
        exit(e.returnValue)



if __name__ == "__main__": main()
