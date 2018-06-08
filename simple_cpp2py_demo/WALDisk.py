===== output.py ==================================================
uint64_t = int


class Block:
    pass


class List:
    def clear(self):
        pass

    def append(self, dev, bid, data):
        pass

    def length(self):
        return 10


class Dict:
    def set(self, dev, bid, data):
        pass


class PartitionAsyncDisk:
    def test_fun(self):
        pass

    def write(self, bid, data):
        pass


class WALDisk:
    def __init__(self, logdisk, datadisks, osync=True):
        self.LOG_MAX_ENTRIES = 10
        self.LOG_BID_HEADER_BLOCK = 0
        self.LOG_DEV_HEADER_BLOCK = 2
        self.LOG_HEADER_BLOCK = 3
        self.PER_BLOCK = 511
        self._osync = osync
        self._logdisk = logdisk
        self._datadisks = datadisks
        self.__recover()
        self._txn = 0
        self._cache = Dict()

    def begin_tx(self):
        if not self._osync and self._txn:
            return
        self._txn.clear()
        self._cache = Dict()

    def write_tx(self, dev, bid, data):
        self._txn.append(dev, bid, data)
        self._logdisk.write(self.LOG_HEADER_BLOCK + self._txn.length(), data)
        self._cache.set(dev, bid, data)

    def __recover(self):
        pass
