import cython
if not cython.compiled:
    from disk import *

from py_exclusive import *    

__all__ = ['BitmapDisk']

# This class is auto-genterated from cpp codes
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
