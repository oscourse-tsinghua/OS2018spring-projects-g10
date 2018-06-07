import cython
if not cython.compiled:
    from disk import *

__all__ = ['WALDisk']

class TripleList:

    def __init__(self):
        self._txn = None
        self._is_none = True
        self.__len__ = 0

    def setNone(self, _is_none):
        self._is_none = _is_none

    def isNone(self):
        return self._is_none

    def isNotNone(self):
        return not self._is_none

    def clear(self):
        self._is_none = False
        self._txn = []
        self.__len__ = 0

    def length(self):
        return len(self._txn)

    def append(self, dev, bid, data):
        self._txn.append([dev, bid, data])
        self.__len__ += 1

    def get(self, idx):
        return self._txn[idx]

    def copy(self):
        new_copy = TripleList()
        new_copy._is_none = self._is_none
        new_copy._txn = self._txn
        new_copy.__len__ = self.__len__
        return new_copy

# This class implements TxnDisk using write-head logging.
# commit() is both atomic and persistent.
# typical use:
# begin_tx() -> write_tx() x N -> flush()
class WALDisk(object):
    LOG_MAX_ENTRIES = 10

    def __init__(self, logdisk, datadisks, osync=True):
        self.LOG_BID_HEADER_BLOCK = 0
        self.LOG_DEV_HEADER_BLOCK = 2
        self.LOG_HEADER_BLOCK = 3

        # Number of pointers in the first header blocks
        self.PER_BLOCK = 511

        self._osync = osync
        self._logdisk = logdisk
        self._datadisks = datadisks[:]
        #print "*********** init WALDisk"
        self.__recover()
        """
        self._txn = None
        """
        self._txn = TripleList()
        self._cache = Dict()

    def begin_tx(self):
        """
        if not self._osync and self._txn is not None:
            return
        """
        if not self._osync and self._txn.isNotNone():
            return

        """
        assert self._txn is None
        """

        """
        self._txn = []
        """
        self._txn.clear()
        self._cache = Dict()

    def write_tx(self, dev, bid, data):
        """
        self._txn.append((dev, bid, data))
        """
        self._txn.append(dev, bid, data)
        """
        self._logdisk.write(self.LOG_HEADER_BLOCK + len(self._txn), data)
        """
        self._logdisk.write(self.LOG_HEADER_BLOCK + self._txn.length(), data)
        self._cache[(dev, bid)] = data

    def write(self, dev, bid, data):
        self._datadisks[dev].write(bid, data)

    def flush(self):
        self.commit_tx(True)

    def commit_tx(self, force=False):
        """
        if self._txn is None:
            return
        """
        if self._txn.isNone():
            return 

        if not self._osync and not force and self._txn.length() <= self.LOG_MAX_ENTRIES - 10:
            return

        """
        assert len(self._txn) <= self.LOG_MAX_ENTRIES, "txn size larger than log"
        """

        """
        txn = self._txn
        """
        txn = self._txn.copy()

        self.writev(txn)
        """
        self._txn = None
        """
        self._txn.setNone(True)

    # pre: log header empty
    #      len(iov) <= LOG_MAX_ENTRIES
    @cython.locals(iov_len='unsigned long long')
    @cython.locals(hdr_bid='Block')
    @cython.locals(hdr_dev='Block')
    @cython.locals(dev='unsigned long long')
    @cython.locals(bid='unsigned long long')
    @cython.locals(block='Block')
    @cython.locals(i='unsigned long long')
    @cython.locals(dd='PartitionAsyncDisk')
    def writev(self, iov):
        """
        iov_len = len(iov)
        """
        iov_len = iov.length()

        if iov_len == 0:
            return
        if iov_len == 1:
            """
            dev, bid, data = iov[0]
            """
            dev, bid, data = iov.get(0)
            dd = self._datadisks[dev]
            dd.write(bid, data)
            # self._datadisks[dev].flush()
            return

        # write log data & build up the header

        hdr_bid1 = ConstBlock(0)
        hdr_dev1 = ConstBlock(0)
        hdr_bid2 = ConstBlock(0)
        hdr_dev2 = ConstBlock(0)

        hdr_bid1[0] = iov_len

        for i in range(iov_len):
            """
            (dev, bid, data) = iov[i]
            """
            (dev, bid, data) = iov.get(i)
            """
            if not self._txn:
            """
            if self._txn.isNone():
                self._logdisk.write(self.LOG_HEADER_BLOCK + 1 + i, data)

            if i < self.PER_BLOCK:
                hdr_bid1.set(i + 1, bid)
                hdr_dev1.set(i + 1, dev)
            else:
                hdr_bid2.set(i - self.PER_BLOCK, bid)
                hdr_dev2.set(i - self.PER_BLOCK, dev)

        self._logdisk.write(self.LOG_DEV_HEADER_BLOCK, hdr_dev1)
        self._logdisk.write(self.LOG_DEV_HEADER_BLOCK + 1, hdr_dev2)
        self._logdisk.write(self.LOG_BID_HEADER_BLOCK + 1, hdr_bid2)

        # make ensure log data reach disk
        self._logdisk.flush()
        # write & flush log header
        self._logdisk.write(self.LOG_BID_HEADER_BLOCK, hdr_bid1)
        self._logdisk.flush()

        # apply log to data disk
        for i in range(iov_len):
            """
            dev, bid, data = iov[i]
            """
            dev, bid, data = iov.get(i)
            # for k in range(len(self._datadisks)):
            #     self._datadisks[dev].write(bid, data, And(dev == k))
            self._datadisks[dev].write(bid, data)
        self.__commit()

    @cython.locals(hdr='Block')
    def __commit(self):
        # make sure data reach disk
        for k in range(len(self._datadisks)):
            self._datadisks[k].flush()
        # delete log
        hdr = ConstBlock(0)
        self._logdisk.write(self.LOG_BID_HEADER_BLOCK, hdr)
        self._logdisk.flush()

    def __recover(self):
        hdr_bid1 = self._logdisk.read(self.LOG_BID_HEADER_BLOCK)
        hdr_dev1 = self._logdisk.read(self.LOG_DEV_HEADER_BLOCK)

        hdr_bid2 = self._logdisk.read(self.LOG_BID_HEADER_BLOCK + 1)
        hdr_dev2 = self._logdisk.read(self.LOG_DEV_HEADER_BLOCK + 1)

        n = hdr_bid1[0]
        # n is symbolic; instead of looping over n, loop over a constant
        for i in range(self.LOG_MAX_ENTRIES):
            if i < self.PER_BLOCK:
                dev = hdr_dev1[1 + i]
                bid = hdr_bid1[1 + i]
            else:
                dev = hdr_dev2[i - self.PER_BLOCK]
                bid = hdr_bid2[i - self.PER_BLOCK]

            data = self._logdisk.read(self.LOG_HEADER_BLOCK + i + 1)
            for k in range(len(self._datadisks)):
                self._datadisks[k].write(bid, data, And(dev == k, ULT(i, n)))
        self.__commit()

    @cython.locals(rdata='Block')
    def read(self, dev, bid):
        rdata = self._datadisks[dev].read(bid)
        return self._cache.get((dev, bid), rdata)

    def _read(self, dev, bid):
        return self.read(dev, bid)

    def crash(self, mach):
        return self.__class__(self._logdisk.crash(mach),
                map(lambda x: x.crash(mach), self._datadisks))
