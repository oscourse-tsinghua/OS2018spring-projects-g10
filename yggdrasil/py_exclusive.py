import cython
if not cython.compiled:
    from disk import *

class PartitionAsyncDiskList(object):

    start = 0

    def __init__(self, datadisks):
        self.datadisks = datadisks

    def __len__(self):
        return len(self.datadisks)

    def __getitem__(self, key):
        return self.datadisks[key]

class TripleList(object):

    start = 0

    def __init__(self, _txn = None):
        self._txn = _txn
        if _txn == None:
            self._is_none = True
        else:
            self._is_none = False

    def setNone(self, _is_none):
        self._is_none = _is_none

    def isNone(self):
        return self._is_none

    def isNotNone(self):
        return not self._is_none

    def clear(self):
        self._is_none = False
        self._txn = []

    def length(self):
        return len(self._txn)

    def append(self, val):
        self._txn.append(val)
    
    def append_triple(self, dev, bid, data):
        self.append([dev, bid, data])

    def get(self, idx):
        return self._txn[idx]

    def get_dev(self, idx):
        return self._txn[idx][0]

    def get_bid(self, idx):
        return self._txn[idx][1]

    def get_data(self, idx):
        return self._txn[idx][2]

    def copy(self):
        new_copy = TripleList()
        new_copy._is_none = self._is_none
        new_copy._txn = self._txn
        return new_copy

    def __iter__(self):
        self.start = 0
        return self

    def next(self):
        if self.start >= len(self._txn):
            raise StopIteration
        else:
            self.start += 1
            return self._txn[self.start - 1]

    def __len__(self):
        return len(self._txn)

    def __getitem__(self, key):
        return self._txn[key]

    def __setitem__(self,key,value):
        self._txn[key] = value

class CacheDict(object):
    def __init__(self):
        self._map = []

    def get(self, gkey, dresult):
        for key, value in self._map:
            try:
                cond = And(*[a == b for a, b in zip(gkey, key)])
            except:
                cond = gkey == key

            dresult = If(cond, value, dresult)
        return dresult

    def has_key(self, gkey):
        res = BoolVal(False)
        for key, _ in self._map:
            try:
                cond = And(*[a == b for a, b in zip(gkey, key)])
            except:
                cond = gkey == key

            res = Or(cond, res)

        return res

    def __setitem__(self, key, value):
        self._map.append((key, value))

    def get3(self, dev, bid, default):
        return self.get((dev, bid), default)

    def set3(self, dev, bid, data):
        return self.__setitem__((dev, bid), data)


