===== output.py ==================================================
uint64_t = int


def Or(a, b):
    return a | b


def USub(a, b):
    return a - b


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


uint64_t = int


class WALDisk:
    LOG_MAX_ENTRIES = None

    def __init__(self, logdisk, datadisks, osync=True):
        pass

    def begin_tx(self):
        pass

    def write_tx(self, dev, bid, data):
        pass

    def write(self, dev, bid, data):
        pass

    def flush(self):
        pass

    def commit_tx(self, force=False):
        pass

    def writev(self, ):
        pass

    def __commit(self):
        pass

    def read(self, dev, bid):
        pass

    def _read(self, dev, bid):
        pass

    def __recover(self):
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


class IndirectInodeDisk:
    NINDIRECT = None

    def __init__(self, idisk):
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

    def bmap(self, vbn):
        pass

    def bunmap(self, vbn):
        pass


class DirLookup:
    pass


class Allocator32:
    def __init__(self, _disk, _start, _end):
        pass

    def alloc(self):
        pass


class Orphans:
    def __init__(self, orphandisk):
        self._orphandisk = orphandisk

    def size(self):
        return self._orphandisk.read(0).__getitem__(0)

    def index(self, idx):
        orphanblock = self._orphandisk.read(0)
        n = orphanblock.__getitem__(0)
        assertion(0 <= n)
        assertion(n < 511)
        np = Extract(8, 0, idx)
        return orphanblock.__getitem__(np + 1)

    def reset(self):
        self._orphandisk.write(0, ConstBlock(0))

    def clear(self, idx):
        orphanblock = self._orphandisk.read(0)
        np = Extract(8, 0, idx)
        orphanblock.__setitem__(np, 0)
        self._orphandisk.write(0, orphanblock)

    def append(self, value):
        orphanblock = self._orphandisk.read(0)
        n = orphanblock.__getitem__(0)
        assertion(0 <= n)
        assertion(n < 511)
        np = Extract(8, 0, n)
        orphanblock.__setitem__(np + 1, value)
        orphanblock.__setitem__(0, n + 1)
        self._orphandisk.write(0, orphanblock)


class MyPIno:
    def __init__(self, _inode):
        self.inode = _inode

    def is_mapped(self, vbn, _inode=0):
        if _inode == 0:
            return self.inode.is_mapped(vbn)
        return _inode.is_mapped(vbn)

    def mappingi(self, vbn, _inode=0):
        if _inode == 0:
            return self.inode.mappingi(vbn)
        return _inode.mappingi(vbn)

    def read(self, bid, _inode=0):
        if _inode == 0:
            return self.inode.read(bid)
        return _inode.read(bid)

    def bmap(self, bid, _inode=0):
        if _inode == 0:
            return self.inode.bmap(bid)
        return _inode.bmap(bid)


class DirImpl:
