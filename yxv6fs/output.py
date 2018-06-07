===== output.py ==================================================
class PartitionAsyncDisk:
    pass


class List:
    def __init__(self):
        self._is_none = True

    def setNone(self, is_none):
        self._is_none = is_none

    def isNone(self):
        return self._is_none

    def isNotNone(self):
        return not self._is_none

    def clear(self):
        self._is_none = False


class TripleList(List):
    pass


class PartitionAsyncDiskList(List):
    pass


class Dict:
    pass


class Block:
    pass


uint64_t = int


class WALDisk:
    def __init__(self, logdisk, datadisks, osync):
        self.LOG_MAX_ENTRIES = 10
        self.LOG_BID_HEADER_BLOCK = 0
        self.LOG_DEV_HEADER_BLOCK = 2
        self.LOG_HEADER_BLOCK = 3
        self.PER_BLOCK = 511
        self._osync = osync
        self._logdisk = logdisk
        self._datadisks = datadisks
        self.__recover()
        self._txn = TripleList()
        self._cache = Dict()

    def __recover(self):
        pass

    def begin_tx(self):
        if not self._osync and self._txn.isNotNone():
            return
        self._txn.clear()
        self._cache = Dict()

    def write_tx(self, dev, bid, data):
        pass

    def flush(self):
        pass

    def commit_tx(self, force):
        pass

    def writev(self, ):
        pass

    def __commit(self):
        pass

    def read(self, dev, bid):
        pass
