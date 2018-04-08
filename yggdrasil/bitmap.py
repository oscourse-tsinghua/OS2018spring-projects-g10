import cython
if not cython.compiled:
    from disk import *

__all__ = ['BitmapDisk']

# Implementation of a bitmap on disk
class BitmapDisk(object):
    def __init__(self, disk):
        self._disk = disk

    # Check if a bit is set
    @cython.locals(mapbit='unsigned long long')
    @cython.locals(mapfield='unsigned long long')
    @cython.locals(mapbid='unsigned long long')
    @cython.locals(block='Block')
    @cython.locals(field='unsigned long long')
    def is_set(self, bit):
        # Define bit as Concat(.., ..)
        mapbit = Extract(6 - 1, 0, bit)
        mapfield = Extract(6 + 9 - 1, 6, bit)
        mapbid = Extract(64 - 1, 6 + 9, bit)

        block = self._disk.read(mapbid)
        field = block[mapfield]

        return Extract(0, 0, field >> Extend(mapbit, 64)) == 1

    @cython.locals(mapbit='unsigned long long')
    @cython.locals(mapfield='unsigned long long')
    @cython.locals(mapbid='unsigned long long')
    @cython.locals(block='Block')
    @cython.locals(field='unsigned long long')
    @cython.locals(new_field='unsigned long long')
    def set_bit(self, bit):
        mapbit = Extract(6 - 1, 0, bit)
        mapfield = Extract(6 + 9 - 1, 6, bit)
        mapbid = Extract(64 - 1, 6 + 9, bit)

        block = self._disk.read(mapbid)

        field = block[mapfield]
        new_field = field | BitVecVal(1, 64) << Extend(mapbit, 64)

        block[mapfield] = new_field
        self._disk.write(mapbid, block)

    @cython.locals(mapbit='unsigned long long')
    @cython.locals(mapfield='unsigned long long')
    @cython.locals(mapbid='unsigned long long')
    @cython.locals(block='Block')
    @cython.locals(field='unsigned long long')
    @cython.locals(new_field='unsigned long long')
    def unset_bit(self, bit):
        mapbit = Extract(6 - 1, 0, bit)
        mapfield = Extract(6 + 9 - 1, 6, bit)
        mapbid = Extract(64 - 1, 6 + 9, bit)

        block = self._disk.read(mapbid)

        field = block[mapfield]
        new_field = field & (~(BitVecVal(1, 64) << Extend(mapbit, 64)))

        block[mapfield] = new_field
        self._disk.write(mapbid, block)

    def crash(self, mach):
        return self.__class__(self._disk.crash(mach))
