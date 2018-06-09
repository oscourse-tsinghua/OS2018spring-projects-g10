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

'''
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
        self._datadisks = datadisks
        #print "*********** init WALDisk"
        self.__recover()
        self._txn = TripleList()
        """
        self._txn = None
        """
        self._cache = CacheDict()

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

        self._txn.clear()
        """
        self._txn = []
        """
        self._cache = CacheDict()

    def write_tx(self, dev, bid, data):
        """
        self._txn.append((dev, bid, data))
        """
        self._txn.append_triple(dev, bid, data)
        """
        self._logdisk.write(self.LOG_HEADER_BLOCK + len(self._txn), data)
        """
        self._logdisk.write(self.LOG_HEADER_BLOCK + self._txn.length(), data)
        #self._cache[(dev, bid)] = data
        self._cache.set3(dev, bid, data)


    def write(self, dev, bid, data):
        #self._datadisks[dev].write(bid, data)
        self._datadisks.__getitem__(dev).write(bid,data)

    def flush(self):
        self.commit_tx(True)



    def commit_tx(self, force=False):
        """
        if self._txn is None:
            return
        """
        if self._txn.isNone():
            return 

        #if not self._osync and not force and len(self._txn) <= self.LOG_MAX_ENTRIES - 10:
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
        #print type(iov)
        """
        if getattr(iov, 'length', False) == False:
            iov = TripleList(iov)
        
        """
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
            dev, bid, data = iov.get_dev(0), iov.get_bid(0), iov.get_data(0)
            #dd = self._datadisks[dev]
            dd = self._datadisks.__getitem__(dev)
            dd.write(bid, data)
            # self._datadisks[dev].flush()
            return

        # write log data & build up the header

        hdr_bid1 = ConstBlock(0)
        hdr_dev1 = ConstBlock(0)
        hdr_bid2 = ConstBlock(0)
        hdr_dev2 = ConstBlock(0)

        #hdr_bid1[0] = iov_len
        hdr_bid1.__setitem__(0, iov_len)

        for i in range(iov_len):
            #(dev, bid, data) = iov[i]
            dev, bid, data = iov.get_dev(i), iov.get_bid(i), iov.get_data(i)
            """
            (dev, bid, data) = iov.get(i)
            """
            """
            if self._txn.isNone():
            """
            #if not self._txn:
            if self._txn.isNone() or self._txn.length() == 0:
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
            #dev, bid, data = iov[i]
            dev, bid, data = iov.get_dev(i), iov.get_bid(i), iov.get_data(i)
            """
            dev, bid, data = iov.get(i)
            """
            # for k in range(len(self._datadisks)):
            #     self._datadisks[dev].write(bid, data, And(dev == k))
            #self._datadisks[dev].write(bid, data)
            self._datadisks.__getitem__(dev).write(bid,data)
        self.__commit()

    @cython.locals(hdr='Block')
    def __commit(self):
        # make sure data reach disk
        """
        for k in range(len(self._datadisks)):
            self._datadisks[k].flush()
        """
        for k in range(self._datadisks.__len__()):
            self._datadisks.__getitem__(k).flush()
        # delete log
        hdr = ConstBlock(0)
        self._logdisk.write(self.LOG_BID_HEADER_BLOCK, hdr)
        self._logdisk.flush()

    def __recover(self):
        hdr_bid1 = self._logdisk.read(self.LOG_BID_HEADER_BLOCK)
        hdr_dev1 = self._logdisk.read(self.LOG_DEV_HEADER_BLOCK)

        hdr_bid2 = self._logdisk.read(self.LOG_BID_HEADER_BLOCK + 1)
        hdr_dev2 = self._logdisk.read(self.LOG_DEV_HEADER_BLOCK + 1)

        #n = hdr_bid1[0]
        n = hdr_bid1.__getitem__(0)
        # n is symbolic; instead of looping over n, loop over a constant
        for i in range(self.LOG_MAX_ENTRIES):
            if i < self.PER_BLOCK:
                """
                dev = hdr_dev1[1 + i]
                bid = hdr_bid1[1 + i]
                """
                dev = hdr_dev1.__getitem__(1 + i)
                bid = hdr_bid1.__getitem__(1 + i)
            else:
                """
                dev = hdr_dev2[i - self.PER_BLOCK]
                bid = hdr_bid2[i - self.PER_BLOCK]
                """
                dev = hdr_dev2.__getitem__(i - self.PER_BLOCK)
                bid = hdr_bid2.__getitem__(i - self.PER_BLOCK)

            data = self._logdisk.read(self.LOG_HEADER_BLOCK + i + 1)
            """
            for k in range(len(self._datadisks)):
                self._datadisks[k].write(bid, data, And(dev == k, ULT(i, n)))
            """
            for k in range(self._datadisks.__len__()):
                self._datadisks.__getitem__(k).write(bid, data, And(dev == k, ULT(i, n)))
        self.__commit()

    @cython.locals(rdata='Block')
    def read(self, dev, bid):
        #rdata = self._datadisks[dev].read(bid)
        rdata = self._datadisks.__getitem__(dev).read(bid)
        #return self._cache.get((dev, bid), rdata)
        return self._cache.get3(dev, bid, rdata)

    def _read(self, dev, bid):
        return self.read(dev, bid)

    def crash(self, mach):
        return self.__class__(self._logdisk.crash(mach),
                map(lambda x: x.crash(mach), self._datadisks))

"""
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
        self.PER_BLOCK = 511


        self.disk = WALDiskImpl(logdisk, datadisks, osync)

    def begin_tx(self):
        self.disk.begin_tx()

    def write_tx(self, dev, bid, data):
        self.disk.write_tx(dev, bid, data)

    def write(self, dev, bid, data):
        self.disk.write(dev, bid, data)

    def flush(self):
        self.disk.flush()

    def commit_tx(self, force=False):
        self.disk.commit_tx(force)

    def writev(self, iov):
        iov_list = TripleList()
        if iov is not None:
            if type(iov) == 'list':
                iov_list._is_none = False
                iov_list._txn = iov
                self.disk.writev(iov_list)
            else:
                self.disk.writev(iov)

    def __commit(self):
        self.disk.__commit()

    def __recover(self):
        self.disk.__recover()

    def read(self, dev, bid):
        return self.disk.read(dev, bid)

    def _read(self, dev, bid):
        return self.disk._read(dev, bid)

    def crash(self, mach):
        return self.disk.crash(mach)
"""

if __name__ == "__main__":
    # just test 
    z = [[1, 2, 3], [4, 5, 6], [1, 1, 1]]
    z_list = TripleList(z)
    print len(z_list)

    z[1] = [3, 3, 3]

    for a, b, c in z_list:
        print a, b, c

    print z[2]
'''
