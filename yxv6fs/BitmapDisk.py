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


class Disk:
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


class BitmapDisk:
    def __init__(self, disk):
        self._disk = disk

    def is_set(self, bit):
        mapbit = Extract(6 - 1, 0, bit)
        mapfield = Extract(6 + 9 - 1, 6, bit)
        mapbid = Extract(64 - 1, 6 + 9, bit)
        block = self._disk.read(mapbid)
        field = block.__getitem__(mapfield)
        return Extract(0, 0, field >> Extend(mapbit, 64)) == 1

    def set_bit(self, bit):
        mapbit = Extract(6 - 1, 0, bit)
        mapfield = Extract(6 + 9 - 1, 6, bit)
        mapbid = Extract(64 - 1, 6 + 9, bit)
        block = self._disk.read(mapbid)
        field = block.__getitem__(mapfield)
        new_field = field | BitVecVal(1, 64) << Extend(mapbit, 64)
        block.__setitem__(mapfield, new_field)
        self._disk.write(mapbid, block)

    def unset_bit(self, bit):
        mapbit = Extract(6 - 1, 0, bit)
        mapfield = Extract(6 + 9 - 1, 6, bit)
        mapbid = Extract(64 - 1, 6 + 9, bit)
        block = self._disk.read(mapbid)
        field = block.__getitem__(mapfield)
        new_field = field & ~(BitVecVal(1, 64) << Extend(mapbit, 64))
        block.__setitem__(mapfield, new_field)
        self._disk.write(mapbid, block)
        
    def crash(self, mach):
        return self.__class__(self._disk.crash(mach))    
