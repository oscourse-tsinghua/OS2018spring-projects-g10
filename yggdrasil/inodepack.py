import cython
if not cython.compiled:
    from disk import *
from collections import namedtuple

from py_exclusive import *    

__all__ = ['InodePackDisk']


# A class that packs multiple inodes together into a single block

# This class is auto-generated from cpp codes
class InodePackDisk:
    def __init__(self, metadisk, datadisk):
        self._disk = metadisk
        self.SIZE = 0
        self.MTIME = 1
        self.MODE = 2
        self.NLINK = 3
        self._UNUSED = 4
        self.OFF = 5

    def read(self, ino):
        return self._disk.read(LShR(ino, 5))

    def set_iattr(self, ino, attr, block=0):
        off = Extract(8, 0, ino * 16)
        bid = LShR(ino, 5)
        if block == 0:
            inode = self._disk.read(bid)
        else:
            inode = block
        inode.__setitem__(self.SIZE + off, attr.size)
        inode.__setitem__(self.MTIME + off, attr.mtime)
        inode.__setitem__(self.MODE + off, attr.mode)
        inode.__setitem__(self.NLINK + off, attr.nlink)
        self._disk.write(bid, inode)

    def get_iattr(self, ino, block=0):
        off = Extract(8, 0, ino * 16)
        bid = LShR(ino, 5)
        if block == 0:
            inode = self._disk.read(bid)
        else:
            inode = block
        stat = Stat(inode.__getitem__(off + self.SIZE), inode.__getitem__(off + self.MTIME), inode.__getitem__(off + self.MODE), inode.__getitem__(off + self.NLINK))
        return stat

    def set_mapping(self, ino, off, ptr, block=0):
        assertion(ULT(off, 11))
        ioff = Extract(8, 0, ino * 16)
        bid = LShR(ino, 5)
        if block == 0:
            old = self._disk.read(bid)
        else:
            old = block
        old.__setitem__(off + ioff + self.OFF, ptr)
        self._disk.write(bid, old)

    def get_mapping(self, ino, off, block=0):
        if off >= 11:
            return 0
        return self._get_mapping(ino, off, block)

    def _get_mapping(self, ino, off, block=0):
        ioff = Extract(8, 0, ino * 16)
        bid = LShR(ino, 5)
        if block == 0:
            block = self._disk.read(bid)
        return block.__getitem__(off + ioff + self.OFF)
        
    def crash(self, mach):
        return self.__class__(self._disk.crash(mach),
                self._disk.crash(mach))