===== output.py ==================================================
uint64_t = int


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
        self._NINDIRECT = IndirectInodeDisk.NINDIRECT
        self._idisk = idisk

    def begin_tx(self):
        self._idisk.commit_tx()

    def commit_tx(self):
        self._idisk.commit_tx()

    def get_iattr(self, ino):
        return self._idisk.get_iattr(ino)

    def set_iattr(self, ino, attr):
        self._idisk.set_iattr(ino, attr)

    def read(self, lbn):
        pass

    def write_tx(self, lbn, data):
        self._idisk.write_tx(lbn, data)

    def write(self, lbn, data):
        self._idisk.write_tx(lbn, data)

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


IndirectInodeDisk.NINDIRECT = 512
