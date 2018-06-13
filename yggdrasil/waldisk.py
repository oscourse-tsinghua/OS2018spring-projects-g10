import cython
if not cython.compiled:
    from disk import *

from py_exclusive import *

__all__ = ['WALDisk']

# note: this class is auto-generated from cpp code
class WALDisk:
    LOG_MAX_ENTRIES = None

    def __init__(self, logdisk, datadisks, osync=True):
        self.LOG_BID_HEADER_BLOCK = 0
        self.LOG_DEV_HEADER_BLOCK = 2
        self.LOG_HEADER_BLOCK = 3
        self.PER_BLOCK = 511
        self._osync = osync
        self._logdisk = logdisk
        self._datadisks = datadisks
        self.__recover()
        self._txn = TripleList()
        self._cache = CacheDict()

    def begin_tx(self):
        if not self._osync and self._txn.isNotNone():
            return
        self._txn.clear()
        self._cache = CacheDict()

    def write_tx(self, dev, bid, data):
        self._txn.append_triple(dev, bid, data)
        self._logdisk.write(self.LOG_HEADER_BLOCK + self._txn.length(), data)
        self._cache.set3(dev, bid, data)

    def write(self, dev, bid, data):
        self._datadisks.__getitem__(dev).write(bid, data)

    def flush(self):
        self.commit_tx(True)

    def commit_tx(self, force=False):
        if self._txn.isNone():
            return
        if not self._osync and not force and self._txn.length() <= WALDisk.LOG_MAX_ENTRIES - 10:
            return
        txn = self._txn.copy()
        self.writev(txn)
        self._txn.setNone(True)

    def writev(self, iov):
        iov_len = iov.length()
        if iov_len == 0:
            return
        if iov_len == 1:
            dev = iov.get_dev(0)
            bid = iov.get_bid(0)
            data = iov.get_data(0)
            dd = self._datadisks.__getitem__(dev)
            dd.write(bid, data)
            return
        hdr_bid1 = ConstBlock(0)
        hdr_dev1 = ConstBlock(0)
        hdr_bid2 = ConstBlock(0)
        hdr_dev2 = ConstBlock(0)
        hdr_bid1.__setitem__(0, iov_len)
        i = 0
        while i < iov_len:
            dev = iov.get_dev(i)
            bid = iov.get_bid(i)
            data = iov.get_data(i)
            if self._txn.isNone() or self._txn.length() == 0:
                self._logdisk.write(self.LOG_HEADER_BLOCK + 1 + i, data)
            if i < self.PER_BLOCK:
                hdr_bid1.set(i + 1, bid)
                hdr_dev1.set(i + 1, dev)
            else:
                hdr_bid2.set(i - self.PER_BLOCK, bid)
                hdr_dev2.set(i - self.PER_BLOCK, dev)
            i += 1
        self._logdisk.write(self.LOG_DEV_HEADER_BLOCK, hdr_dev1)
        self._logdisk.write(self.LOG_DEV_HEADER_BLOCK + 1, hdr_dev2)
        self._logdisk.write(self.LOG_BID_HEADER_BLOCK + 1, hdr_bid2)
        self._logdisk.flush()
        self._logdisk.write(self.LOG_BID_HEADER_BLOCK, hdr_bid1)
        self._logdisk.flush()
        i = 0
        while i < iov_len:
            dev = iov.get_dev(i)
            bid = iov.get_bid(i)
            data = iov.get_data(i)
            self._datadisks.__getitem__(dev).write(bid, data)
            i += 1
        self.__commit()

    def __commit(self):
        k = 0
        while k < self._datadisks.__len__():
            self._datadisks.__getitem__(k).flush()
            k += 1
        hdr = ConstBlock(0)
        self._logdisk.write(self.LOG_BID_HEADER_BLOCK, hdr)
        self._logdisk.flush()

    def read(self, dev, bid):
        rdata = self._datadisks.__getitem__(dev).read(bid)
        return self._cache.get3(dev, bid, rdata)

    def _read(self, dev, bid):
        return self.read(dev, bid)

    def __recover(self):
        hdr_bid1 = self._logdisk.read(self.LOG_BID_HEADER_BLOCK)
        hdr_dev1 = self._logdisk.read(self.LOG_DEV_HEADER_BLOCK)
        hdr_bid2 = self._logdisk.read(self.LOG_BID_HEADER_BLOCK + 1)
        hdr_dev2 = self._logdisk.read(self.LOG_DEV_HEADER_BLOCK + 1)
        n = hdr_bid1.__getitem__(0)
        i = 0
        while i < WALDisk.LOG_MAX_ENTRIES:
            dev = 0
            bid = 0
            if i < self.PER_BLOCK:
                dev = hdr_dev1.__getitem__(1 + i)
                bid = hdr_bid1.__getitem__(1 + i)
            else:
                dev = hdr_dev2.__getitem__(i - self.PER_BLOCK)
                bid = hdr_bid1.__getitem__(i - self.PER_BLOCK)
            data = self._logdisk.read(self.LOG_HEADER_BLOCK + i + 1)
            k = 0
            while k < self._datadisks.__len__():
                self._datadisks.__getitem__(k).write(bid, data, And(dev == k, ULT(i, n)))
                k += 1
            i += 1
        self.__commit()

    def crash(self, mach):
        return self.__class__(self._logdisk.crash(mach),
                map(lambda x: x.crash(mach), self._datadisks))

WALDisk.LOG_MAX_ENTRIES = 10
