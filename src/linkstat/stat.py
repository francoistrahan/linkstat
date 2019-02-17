from collections import defaultdict
from itertools import chain
from os import stat, walk
from os.path import isfile, join



class Stat:
    def __init__(self, folders, exclude):
        self.folders = folders
        self.exclude = exclude
        self.sets = { }
        self.actions = {
            Actions.OR: self.do_or,
            Actions.AND: self.do_and,
            Actions.UNIQUE: self.do_unique,
            }


    def listInodesAndFiles(self, folder):
        for dirpath, dirnames, filenames in walk(folder, followlinks=False):
            for fn in filenames:
                if not any(r.match(fn) for r in self.exclude):
                    fp = join(dirpath, fn)
                    if isfile(fp):
                        inode = Stat(fp).st_ino
                        yield inode, fp


    def buildSet(self, folder):
        fs = defaultdict(lambda: list())
        for inode, fp in self.listInodesAndFiles(folder):
            fs[inode].append(fp)
        self.sets[folder] = fs


    def run(self, action):
        for fp in self.folders:
            self.buildSet(fp)

        self.actions[action]()

        folders = sorted(self.folders)
        result = defaultdict(lambda: [])
        for inode in sorted(self.result_inodes):
            for folder in folders:
                iandfs = self.sets[folder]
                try:
                    fs = iandfs[inode]
                except KeyError:
                    pass
                else:
                    for f in sorted(fs):
                        result[inode].append(f)
        self.result = result


    def do_or(self):
        sets = [set(iandfs.keys()) for iandfs in self.sets.values()]
        first = sets.pop(0)
        self.result_inodes = first.union(*sets)


    def do_and(self):
        sets = [set(iandfs.keys()) for iandfs in self.sets.values()]
        first = sets.pop(0)
        self.result_inodes = first.intersection(*sets)


    def do_unique(self):
        counts = defaultdict(lambda: 0)
        for inode in chain(*(iandfs.keys() for iandfs in self.sets.values())):
            counts[inode] += 1

        self.result_inodes = list(inode for inode, count in counts.items() if count == 1)



from . import Actions
