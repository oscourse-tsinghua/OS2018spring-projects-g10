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
    def __init__(self, size, mtime, mode, nlink):
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

    def bmap(self, vbn):
        pass

    def bunmap(self, vbn):
        pass


class errno:
    ENOSPC = None
    ENOENT = None
    ENOTDIR = None


ENOSPC = None

ENOENT = None

ENOTDIR = None


class Allocator32:
    def __init__(self, _disk, _start, _end):
        pass

    def alloc(self):
        pass


class Orphans:
    def __init__(self, orphandisk):
        self._orphandisk = orphandisk

    def size(self):
        return self._orphandisk.read(0).__getitem__(0)

    def index(self, idx):
        orphanblock = self._orphandisk.read(0)
        n = orphanblock.__getitem__(0)
        assertion(0 <= n)
        assertion(n < 511)
        np = Extract(8, 0, idx)
        return orphanblock.__getitem__(np + 1)

    def reset(self):
        self._orphandisk.write(0, ConstBlock(0))

    def clear(self, idx):
        orphanblock = self._orphandisk.read(0)
        np = Extract(8, 0, idx)
        orphanblock.__setitem__(np, 0)
        self._orphandisk.write(0, orphanblock)

    def append(self, value):
        orphanblock = self._orphandisk.read(0)
        n = orphanblock.__getitem__(0)
        assertion(0 <= n)
        assertion(n < 511)
        np = Extract(8, 0, n)
        orphanblock.__setitem__(np + 1, value)
        orphanblock.__setitem__(0, n + 1)
        self._orphandisk.write(0, orphanblock)


class MyPIno:
    def __init__(self, _inode):
        self.inode = _inode

    def is_mapped(self, vbn, _inode=0):
        if _inode == 0:
            return self.inode.is_mapped(vbn)
        return _inode.is_mapped(vbn)

    def mappingi(self, vbn, _inode=0):
        if _inode == 0:
            return self.inode.mappingi(vbn)
        return _inode.mappingi(vbn)

    def read(self, bid, _inode=0):
        if _inode == 0:
            return self.inode.read(bid)
        return _inode.read(bid)

    def bmap(self, bid, _inode=0):
        if _inode == 0:
            return self.inode.bmap(bid)
        return _inode.bmap(bid)


class Tuple2:
    def __init__(self, _a, _b):
        pass

    def __getitem__(self, idx):
        pass


class Tuple3:
    def __init__(self, block, _bid, _off):
        pass

    def get_bid(self):
        pass

    def get_off(self):
        pass

    def get_block(self):
        pass


class Tuple4:
    def __init__(self, block, _bid, _off, _valid):
        pass

    def get_bid(self):
        pass

    def get_off(self):
        pass

    def get_block(self):
        pass

    def get_valid(self):
        pass


class NameType:
    def __getitem__(self, idx):
        pass


class DirLook:
    def __init__(self, pino):
        pass

    def locate_dentry_ino(self, ino, name):
        pass

    def locate_empty_slot_ino(self, ino):
        pass


class DirImpl:
    NBLOCKS = None
    IFREEDISK = None
    ORPHANS = None

    def __init__(self, txndisk, inode):
        self._txndisk = txndisk
        self._inode = inode
        self._dirlook = DirLook(MyPIno(inode))
        self._ifree = Disk(DirImpl.IFREEDISK, self._txndisk)
        orphandisk = Disk(DirImpl.ORPHANS, self._txndisk)
        self._iallocator = Allocator32(self._ifree, 0, 1024)
        self._ibitmap = Bitmap(self._ifree)
        self._orphans = Orphans(orphandisk)

    def locate_dentry_ino(self, ino, name):
        tuple = self._dirlook.locate_dentry_ino(ino, name)
        ioff = tuple.__getitem__(0)
        off = tuple.__getitem__(1)
        assertion(ULT(ioff, 522))
        assertion(ioff != 10)
        bid = self._inode.bmap(Concat32(ino, ioff))
        block = self._inode.read(bid)
        valid = And(bid != 0, off % 16 == 0, Extract(31, 0, block.__getitem__(off)) != 0)
        i = 0
        while i < 15:
            valid = And(valid, block.__getitem__(off + i + 1) == name.__getitem__(i))
            i += 1
        return Tuple4(block, bid, off, valid)

    def locate_empty_dentry_slot_ino(self, ino):
        tuple = self._dirlook.locate_empty_slot_ino(ino)
        ioff = tuple.__getitem__(0)
        off = tuple.__getitem__(1)
        assertion(ULT(ioff, 522))
        assertion(ioff != 10)
        bid = self._inode.bmap(Concat32(ino, ioff))
        block = self._inode.read(bid)
        assertion(bid != 0)
        assertion(off % 16 == 0)
        assertion(block.__getitem__(off) == 0)
        return Tuple3(block, bid, off)

    def locate_empty_dentry_slot_err_ino(self, ino):
        tuple = self._dirlook.locate_empty_slot_ino(ino)
        ioff = tuple.__getitem__(0)
        off = tuple.__getitem__(1)
        assertion(ULT(ioff, 522))
        assertion(ioff != 10)
        bid = self._inode.bmap(Concat32(ino, ioff))
        block = self._inode.read(bid)
        return Tuple4(block, bid, off, And(bid != 0, off % 16 == 0, block.__getitem__(off) == 0))

    def write_dentry(self, block, off, ino, name):
        block.__setitem__(off, ino)
        i = 0
        while i < 15:
            block.__setitem__(off + i + 1, name.__getitem__(i))
            i += 1

    def clear_dentry(self, block, off):
        i = 0
        while i < 16:
            block.__setitem__(off + i, 0)
            i += 1

    def ialloc(self):
        ino = self._iallocator.alloc()
        assertion(ino != 0)
        assertion(self.is_ifree(ino))
        self._ibitmap.set_bit(ino)
        return ino

    def is_ifree(self, ino):
        return Not(self._ibitmap.is_set(ino))

    def is_valid(self, ino):
        return And(ino != 0, self._ibitmap.is_set(ino), UGT(self.get_iattr(ino).nlink, 0))

    def is_gcable(self, ino):
        return And(ino != 0, self._ibitmap.is_set(ino), self.get_iattr(ino).nlink == 0)

    def is_dir(self, ino):
        attr = self._inode.get_iattr(ino)
        return And(self.is_valid(ino), (attr.mode & S_IFDIR) != 0)

    def is_regular(self, ino):
        attr = self._inode.get_iattr(ino)
        return And(self.is_valid(ino), (attr.mode & S_IFDIR) == 0)

    def get_iattr(self, ino):
        return self._inode.get_iattr(ino)

    def set_iattr(self, ino, attr):
        self._inode.begin_tx()
        self._inode.set_iattr(ino, attr)
        self._inode.commit_tx()

    def read(self, ino, blocknum):
        attr = self.get_iattr(ino)
        bsize = attr.bsize
        is_mapped = self._inode.is_mapped(Concat32(ino, blocknum))
        lbn = self._inode.mappingi(Concat32(ino, blocknum))
        res = self._inode.read(lbn)
        zeroblock = ConstBlock(0)
        return If(And(is_mapped, ULT(blocknum, bsize)), res, zeroblock)

    def truncate(self, ino, fsize):
        target_bsize = fsize / 4096 + (fsize % 4096 != 0)
        attr = self._inode.get_iattr(ino)
        while attr.bsize > target_bsize:
            self._inode.begin_tx()
            self._inode.bunmap(Concat32(ino, attr.bsize - 1))
            attr.size = Concat32(attr.bsize - 1, fsize)
            self._inode.set_iattr(ino, attr)
            self._inode.commit_tx()
        if attr.fsize > fsize:
            self._inode.begin_tx()
            attr.size = Concat32(attr.bsize, fsize)
            self._inode.set_iattr(ino, attr)
            self._inode.commit_tx()

    def write(self, ino, blocknum, v, size=BitVecVal(4096, 32)):
        assertion(ULT(blocknum, 522))
        assertion(ULT(BitVecVal(0, 32), size))
        assertion(ULE(size, BitVecVal(4096, 32)))
        assertion(self.is_regular(ino))
        self._inode.begin_tx()
        bid = self._inode.bmap(Concat32(ino, blocknum))
        self._inode.write(bid, v)
        attr = self._inode.get_iattr(ino)
        nsize = Concat32(blocknum + 1, blocknum * 4096 + size)
        update = ULE(attr.fsize, blocknum * 4096 + size)
        attr.size = If(update, nsize, attr.size)
        self._inode.set_iattr(ino, attr)
        self._inode.commit_tx()
        return size

    def lookup(self, parent, name):
        assertion(self.is_dir(parent))
        self._inode.begin_tx()
        tp = self.locate_dentry_ino(parent, name)
        parent_block = tp.get_block()
        off = tp.get_off()
        valid = tp.get_valid()
        self._inode.commit_tx()
        return If(valid, Extract(31, 0, parent_block.__getitem__(off)), 0)

    def mknod(self, parent, name, mode, mtime):
        assertion(self.is_dir(parent))
        assertion(name.__getitem__(0) != 0)
        self._inode.begin_tx()
        tp = self.locate_empty_dentry_slot_err_ino(parent)
        parent_block = tp.get_block()
        parent_bid = tp.get_bid()
        off = tp.get_off()
        valid = tp.get_valid()
        if Not(valid):
            self._inode.commit_tx()
            return Tuple2(0, errno.ENOSPC)
        ino = self.ialloc()
        attr = Stat(0, mtime, mode, 2)
        self._inode.set_iattr(ino, attr)
        attr = self._inode.get_iattr(parent)
        assertion(ULE(attr.bsize, 522))
        attr.size = Concat32(BitVecVal(522, 32), BitVecVal(4096 * 522, 32))
        assertion(ULT(attr.nlink, attr.nlink + 1))
        attr.nlink += 1
        self._inode.set_iattr(parent, attr)
        self.write_dentry(parent_block, off, ino, name)
        parent_block.__setitem__(off, ino)
        self._inode.write(parent_bid, parent_block)
        self._inode.commit_tx()
        return Tuple2(ino, 0)

    def unlink(self, parent, name):
        assertion(self.is_dir(parent))
        assertion(name.__getitem__(0) != 0)
        self._inode.begin_tx()
        tp = self.locate_dentry_ino(parent, name)
        parent_block = tp.get_block()
        parent_bid = tp.get_bid()
        off = tp.get_off()
        valid = tp.get_valid()
        assertion(valid)
        attr = self._inode.get_iattr(parent)
        assertion(UGE(attr.nlink, 2))
        attr.nlink -= 1
        self._inode.set_iattr(parent, attr)
        ino = Extract(31, 0, parent_block.__getitem__(off))
        attr = self._inode.get_iattr(ino)
        attr.nlink = 1
        self._inode.set_iattr(ino, attr)
        self.clear_dentry(parent_block, off)
        self._inode.write(parent_bid, parent_block)
        self._orphans.append(Extend(ino, 64))
        self._inode.commit_tx()
        return ino

    def rmdir(self, parent, name):
        assertion(self.is_dir(parent))
        assertion(name.__getitem__(0) != 0)
        self._inode.begin_tx()
        tp = self.locate_dentry_ino(parent, name)
        parent_block = tp.get_block()
        parent_bid = tp.get_bid()
        off = tp.get_off()
        valid = tp.get_valid()
        if Not(valid):
            self._inode.commit_tx()
            return Tuple2(0, errno.ENOENT)
        assertion(valid)
        ino = Extract(31, 0, parent_block.__getitem__(off))
        if Not(self.is_dir(ino)):
            self._inode.commit_tx()
            return Tuple2(0, errno.ENOTDIR)
        attr = self._inode.get_iattr(parent)
        assertion(UGE(attr.nlink, 2))
        attr.nlink -= 1
        self._inode.set_iattr(parent, attr)
        self.clear_dentry(parent_block, off)
        self._inode.write(parent_bid, parent_block)
        attr = self._inode.get_iattr(ino)
        attr.nlink = 1
        self._inode.set_iattr(ino, attr)
        self._orphans.append(Extend(ino, 64))
        self._inode.commit_tx()
        return Tuple2(ino, 0)

    def rename(self, oparent, oname, nparent, nname):
        assertion(self.is_dir(oparent))
        assertion(self.is_dir(nparent))
        assertion(oname.__getitem__(0) != 0)
        assertion(nname.__getitem__(0) != 0)
        self._inode.begin_tx()
        attr = self._inode.get_iattr(oparent)
        assertion(UGE(attr.nlink, 2))
        attr.nlink -= 1
        self._inode.set_iattr(oparent, attr)
        attr = self._inode.get_iattr(nparent)
        assertion(ULE(attr.bsize, 522))
        attr.size = Concat32(BitVecVal(522, 32), BitVecVal(4096 * 522, 32))
        assertion(ULT(attr.nlink, attr.nlink + 1))
        attr.nlink += 1
        self._inode.set_iattr(nparent, attr)
        tp = self.locate_dentry_ino(oparent, oname)
        oparent_block = tp.get_block()
        oparent_bid = tp.get_bid()
        ooff = tp.get_off()
        ovalid = tp.get_valid()
        assertion(ovalid)
        ino = oparent_block.__getitem__(ooff)
        self.clear_dentry(oparent_block, ooff)
        self._inode.write(oparent_bid, oparent_block)
        tp = self.locate_dentry_ino(nparent, nname)
        nparent_block = tp.get_block()
        nparent_bid = tp.get_bid()
        noff = tp.get_off()
        nvalid = tp.get_valid()
        if nvalid:
            self._orphans.append(nparent_block.__getitem__(noff))
            self.clear_dentry(nparent_block, noff)
        tp3 = self.locate_empty_dentry_slot_ino(nparent)
        nparent_block = tp3.get_block()
        nparent_bid = tp3.get_bid()
        noff = tp3.get_off()
        self.write_dentry(nparent_block, noff, ino, nname)
        self._inode.write(nparent_bid, nparent_block)
        self._inode.commit_tx()
        return 0

    def forget(self, ino):
        if Or((self.get_iattr(ino).mode & S_IFDIR) != 0, self.get_iattr(ino).nlink != 1):
            return
        assertion(self.is_regular(ino))
        self._inode.begin_tx()
        attr = self._inode.get_iattr(ino)
        attr.nlink = 0
        self._inode.set_iattr(ino, attr)
        self._inode.commit_tx()

    def fsync(self):
        self._txndisk.flush()

    def gc1(self, orph_index, off):
        ino = Extract(31, 0, self._orphans.index(orph_index))
        if not self.is_gcable(ino):
            return
        self._inode.begin_tx()
        self._inode.bunmap(Concat32(ino, off))
        nsize = off
        attr = self._inode.get_iattr(ino)
        if attr.bsize == nsize + 1:
            attr.size = Concat32(nsize, nsize * 4096)
            self._inode.set_iattr(ino, attr)
        self._inode.commit_tx()

    def gc2(self, orph_index):
        ino = Extract(31, 0, self._orphans.index(orph_index))
        if not self.is_gcable(ino):
            return
        if self._inode.get_iattr(ino).size == 0:
            self._inode.begin_tx()
            self._orphans.clear(orph_index)
            self._ibitmap.unset_bit(ino)
            self._inode.commit_tx()

    def gc3(self):
        self._inode.begin_tx()
        self._orphans.reset()
        self._inode.commit_tx()


S_IFDIR = None

DirImpl.NBLOCKS = 522

DirImpl.IFREEDISK = 4

DirImpl.ORPHANS = 5
