===== output.py ==================================================
uint64_t = int


def Or(a, b):
    return a | b


def USub(a, b):
    return a - b


def LShR(a, b):
    return a >> b


def Concat32(a, b):
    return (a << 32) | b


def If(cond, a, b):
    if cond:
        return a
    return b


def Extract(hi, lo, val):
    return val >> lo & ((1 << (hi - lo + 1)) - 1)


def And(a=1, b=1, c=1):
    return (a and b) and c


def ULT(a, b):
    return a < b


class Block:
    def __setitem__(self, key, val):
        pass

    def __getitem__(self, key):
        pass

    def set(self, key, val):
        pass

    def get(self, key):
        pass


def ConstBlock(val):
    return Block()


class PartitionAsyncDisk:
    def write(self, blknum, block, cond=1):
        pass

    def read(self, blknum):
        return Block()

    def flush(self):
        pass


class PartitionAsyncDiskList:
    def __len__(self):
        return 10

    def __getitem__(self, key):
        return PartitionAsyncDisk()


class TripleList:
    def setNone(self, _is_none):
        pass

    def isNone(self):
        pass

    def isNotNone(self):
        pass

    def clear(self):
        pass

    def length(self):
        return 10

    def append_triple(self, dev, bid, data):
        pass

    def get_dev(self, idx):
        pass

    def get_bid(self, idx):
        pass

    def get_data(self, idx):
        pass

    def copy(self):
        pass

    def __len__(self):
        return 10


class CacheDict:
    def get3(self, dev, bid, dresult):
        return dresult

    def set3(self, dev, bid, data):
        pass


class Disk:
    def __init__(self, _dev, _txndisk):
        pass

    def read(self, bid):
        pass

    def write(self, bid, data):
        pass


class Allocator64:
    def __init__(self, _txndisk, _dev, _start, _end):
        pass

    def alloc(self):
        pass


class Bitmap:
    def __init__(self, _disk):
        pass

    def is_set(self, lbn):
        pass

    def set_bit(self, lbn):
        pass

    def unset_bit(self, lbn):
        pass

    def mkfs(self):
        pass


class Stat:
    def __init__(self, size, mtime, mode, nlink):
        pass


class InodePack:
    def __init__(self, _inodemeta, inodedata):
        pass

    def get_iattr(self, ino):
        pass

    def set_iattr(self, ino, attr):
        pass

    def get_mapping(self, ino, eoff, block=0):
        pass

    def set_mapping(self, ino, off, ptr, block=0):
        pass

    def read(self, ino):
        pass

    def mkfs(self):
        pass


class InodeDisk:
    FREEDISK = None
    INODEMETADISK = None
    INODEDATADISK = None
    DATADISK = None
    NDIRECT = None

    def __init__(self, txndisk):
        pass

    def begin_tx(self):
        pass

    def commit_tx(self):
        pass

    def get_iattr(self, ino):
        pass

    def set_iattr(self, ino, attr):
        pass

    def read(self, lbn):
        pass

    def write_tx(self, lbn, data):
        pass

    def write(self, lbn, data):
        pass

    def mappingi(self, vbn):
        pass

    def is_mapped(self, vbn):
        pass

    def is_free(self, vbn):
        pass

    def alloc(self):
        pass

    def free(self, lbn):
        pass

    def bmap(self, vbn):
        pass

    def bunmap(self, vbn):
        pass

    def mkfs(self):
        pass


uint64_t = int


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
