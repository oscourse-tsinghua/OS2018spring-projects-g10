#include "DirImpl.h"

static uint64_t S_IFDIR;

uint64_t DirImpl::NBLOCKS = 522;
uint64_t DirImpl::IFREEDISK = 4;
uint64_t DirImpl::ORPHANS = 5;

inline Block* If(int cond, Block *a, Block* b);

inline int Not(int a);
DirImpl::DirImpl(WALDisk *txndisk, IndirectInodeDisk *inode) {
	_txndisk = txndisk;
	_inode = inode;
	_dirlook = new DirLook(new MyPIno(inode));
	_ifree = new Disk(IFREEDISK, _txndisk);
	Disk *orphandisk = new Disk(ORPHANS, _txndisk);
	_iallocator = new Allocator32(_ifree, 0, 1024);
	_ibitmap = new Bitmap(_ifree);
	_orphans = new Orphans(orphandisk);
}

Tuple4* DirImpl::locate_dentry_ino(uint64_t ino, NameType *name) {
	Tuple2 *tuple = _dirlook->locate_dentry_ino(ino, name);
	uint64_t ioff = tuple->__getitem__(0);
	uint64_t off = tuple->__getitem__(1);
	assertion(ULT(ioff, 522));
	assertion(ioff != 10);
	uint64_t bid = _inode->bmap(Concat32(ino, ioff));
	Block *block = _inode->read(bid);
	int valid = And(bid != 0, off % 16 == 0, Extract(31, 0, block->__getitem__(off)) != 0);
	for (int i = 0; i < 15; ++ i) {
            valid = And(valid, block->__getitem__(off + i + 1) == name->__getitem__(i));
	}
	return new Tuple4(block, bid, off, valid);
}

Tuple3* DirImpl::locate_empty_dentry_slot_ino(uint64_t ino) {
	Tuple2 *tuple = _dirlook->locate_empty_slot_ino(ino);
	uint64_t ioff = tuple->__getitem__(0);
	uint64_t off = tuple->__getitem__(1);
	assertion(ULT(ioff, 522));
	assertion(ioff != 10);
	uint64_t bid = _inode->bmap(Concat32(ino, ioff));
	Block *block = _inode->read(bid);
	assertion(bid != 0);
	assertion(off % 16 == 0);
	assertion(block->__getitem__(off) == 0);
	return new Tuple3(block, bid, off);
}

Tuple4* DirImpl::locate_empty_dentry_slot_err_ino(uint64_t ino) {
	Tuple2 *tuple = _dirlook->locate_empty_slot_ino(ino);
	uint64_t ioff = tuple->__getitem__(0);
	uint64_t off = tuple->__getitem__(1);
	assertion(ULT(ioff, 522));
	assertion(ioff != 10);
	uint64_t bid = _inode->bmap(Concat32(ino, ioff));
	Block *block = _inode->read(bid);
        return new Tuple4(block, bid, off, And(bid != 0, off % 16 == 0, block->__getitem__(off) == 0));
}

void DirImpl::write_dentry(Block *block, uint64_t off, uint64_t ino, NameType *name) {
	block->__setitem__(off, ino);
	for (int i = 0; i < 15; ++ i) {
		block->__setitem__(off + i + 1, name->__getitem__(i));
	}
}

void DirImpl::clear_dentry(Block *block, uint64_t off) {
	for (int i = 0; i < 16; ++ i) {
		block->__setitem__(off + i, 0);
	}
}

uint64_t DirImpl::ialloc() {
	uint64_t ino = _iallocator->alloc();
	assertion(ino != 0);
	assertion(is_ifree(ino));
	_ibitmap->set_bit(ino);
	return ino;
}

int DirImpl::is_ifree(uint64_t ino) {
	return Not(_ibitmap->is_set(ino));
}

int DirImpl::is_valid(uint64_t ino) {
        return And(ino != 0, _ibitmap->is_set(ino), UGT(get_iattr(ino)->nlink, 0));
}

int DirImpl::is_gcable(uint64_t ino) {
        return And(ino != 0, _ibitmap->is_set(ino), get_iattr(ino)->nlink == 0);
}

int DirImpl::is_dir(uint64_t ino){
	Stat *attr = _inode->get_iattr(ino);
	return And(is_valid(ino), (attr->mode & S_IFDIR) != 0);
}

int DirImpl::is_regular(uint64_t ino) {
	Stat *attr = _inode->get_iattr(ino);
	return And(is_valid(ino), (attr->mode & S_IFDIR) == 0);
}

Stat* DirImpl::get_iattr(uint64_t ino) {
	return _inode->get_iattr(ino);
}

void DirImpl::set_iattr(uint64_t ino, Stat *attr) {
	_inode->begin_tx();
	_inode->set_iattr(ino, attr);
	_inode->commit_tx();
}

Block *DirImpl::read(uint64_t ino, uint64_t blocknum) {
	Stat *attr = get_iattr(ino);
	uint64_t bsize = attr->bsize;

	int is_mapped = _inode->is_mapped(Concat32(ino, blocknum));
	uint64_t lbn = _inode->mappingi(Concat32(ino, blocknum));
	Block* res = _inode->read(lbn);
	Block* zeroblock = ConstBlock(0);
	return If(And(is_mapped, ULT(blocknum, bsize)), res, zeroblock);
}

void DirImpl::truncate(uint64_t ino, uint64_t fsize) {
	uint64_t target_bsize = fsize / 4096 + (fsize % 4096 != 0);

	Stat *attr = _inode->get_iattr(ino);

	while (attr->bsize > target_bsize) {
		_inode->begin_tx();
		_inode->bunmap(Concat32(ino, attr->bsize - 1));
		attr->size = Concat32(attr->bsize - 1, fsize);
		_inode->set_iattr(ino, attr);
		_inode->commit_tx();
	}

	if (attr->fsize > fsize) {
		_inode->begin_tx();
		attr->size = Concat32(attr->bsize, fsize);
		_inode->set_iattr(ino, attr);
		_inode->commit_tx();
	}
}

uint64_t DirImpl::write(uint64_t ino, uint64_t blocknum, Block* v, uint64_t size) {
	assertion(ULT(blocknum, 522));
	assertion(ULT(BitVecVal(0, 32), size));
	assertion(ULE(size, BitVecVal(4096, 32)));
	assertion(is_regular(ino));
	_inode->begin_tx();
	uint64_t bid = _inode->bmap(Concat32(ino, blocknum));
	_inode->write(bid, v);
	Stat *attr = _inode->get_iattr(ino);
	uint64_t nsize = Concat32(blocknum + 1, blocknum * 4096 + size);
	int update = ULE(attr->fsize, blocknum * 4096 + size);
	attr->size = If(update, nsize, attr->size);
	_inode->set_iattr(ino, attr);
	_inode->commit_tx();
	return size;
}

uint64_t DirImpl::lookup(uint64_t parent, NameType *name) {
	assertion(is_dir(parent));
	_inode->begin_tx();
	Tuple4 *tp = locate_dentry_ino(parent, name);
	/*
	Block *parent_block = tp->__getitem__(0);
	uint64_t off = tp->__getitem__(1);
	int valid = tp->__getitem__(2);
	*/
	Block *parent_block = tp->get_block();
	uint64_t off = tp->get_off();
	int valid = tp->get_valid();
	_inode->commit_tx();
	return If(valid, Extract(31, 0, parent_block->__getitem__(off)), 0);
}

Tuple2* DirImpl::mknod(uint64_t parent, NameType *name, uint64_t mode, uint64_t mtime) {
	assertion(is_dir(parent));
	assertion(name->__getitem__(0) != 0);
	_inode->begin_tx();
	Tuple4 *tp = locate_empty_dentry_slot_err_ino(parent);
	Block *parent_block = tp->get_block();
	uint64_t parent_bid = tp->get_bid();
	uint64_t off = tp->get_off();
	int valid = tp->get_valid();
	if (Not(valid)) {
		_inode->commit_tx();
		return new Tuple2(0, errno::ENOSPC);
	}
	uint64_t ino = ialloc();
	Stat *attr = new Stat(0, mtime, mode, 2);
	_inode->set_iattr(ino, attr);
	attr = _inode->get_iattr(parent);
	
	assertion(ULE(attr->bsize, 522));
	attr->size = Concat32(BitVecVal(522, 32), BitVecVal(4096 * 522, 32));
	assertion(ULT(attr->nlink, attr->nlink + 1));
	attr->nlink += 1;
	_inode->set_iattr(parent, attr);
	write_dentry(parent_block, off, ino, name);
	parent_block->__setitem__(off, ino);
	_inode->write(parent_bid, parent_block);
	_inode->commit_tx();
	return new Tuple2(ino, 0);
}

uint64_t DirImpl::unlink(uint64_t parent, NameType *name) {
	assertion(is_dir(parent));
	assertion(name->__getitem__(0) != 0);
	_inode->begin_tx();
	Tuple4 *tp = locate_dentry_ino(parent, name);
	Block *parent_block = tp->get_block();
	uint64_t parent_bid = tp->get_bid();
	uint64_t off = tp->get_off();
	int valid = tp->get_valid();

	assertion(valid);

	Stat *attr = _inode->get_iattr(parent);
	assertion(UGE(attr->nlink, 2));
	attr->nlink -= 1;
	_inode->set_iattr(parent, attr);

	uint64_t ino = Extract(31, 0, parent_block->__getitem__(off));
	attr = _inode->get_iattr(ino);
	attr->nlink = 1;
	_inode->set_iattr(ino, attr);
	clear_dentry(parent_block, off);
	_inode->write(parent_bid, parent_block);
	_orphans->append(Extend(ino, 64));
	_inode->commit_tx();
	return ino;

}

Tuple2* DirImpl::rmdir(uint64_t parent, NameType *name) {
	assertion(is_dir(parent));
	assertion(name->__getitem__(0) != 0);
	_inode->begin_tx();
	Tuple4 *tp = locate_dentry_ino(parent, name);
	Block *parent_block = tp->get_block();
	uint64_t parent_bid = tp->get_bid();
	uint64_t off = tp->get_off();
	int valid = tp->get_valid();

	if (Not(valid)) {
		_inode->commit_tx();
		return new Tuple2(0, errno::ENOENT);
	}
	assertion(valid);
	uint64_t ino = Extract(31, 0, parent_block->__getitem__(off));
	if (Not(is_dir(ino))) {
		_inode->commit_tx();
		return new Tuple2(0, errno::ENOTDIR);
	}

	Stat *attr = _inode->get_iattr(parent);
	assertion(UGE(attr->nlink, 2));
	attr->nlink -= 1;
	_inode->set_iattr(parent, attr);

	clear_dentry(parent_block, off);
	_inode->write(parent_bid, parent_block);

	attr = _inode->get_iattr(ino);
	attr->nlink = 1;
	_inode->set_iattr(ino, attr);

	_orphans->append(Extend(ino, 64));

	_inode->commit_tx();

	return new Tuple2(ino, 0);
}

void DirImpl::forget(uint64_t ino) {
	if (Or((get_iattr(ino)->mode & S_IFDIR) != 0, get_iattr(ino)->nlink != 1)) {
		return ;
	}
	assertion(is_regular(ino));

	_inode->begin_tx();
	Stat *attr = _inode->get_iattr(ino);
	attr->nlink = 0;
	_inode->set_iattr(ino, attr);
	_inode->commit_tx();
}

uint64_t DirImpl::rename(uint64_t oparent, NameType *oname, uint64_t nparent, NameType *nname) {
	assertion(is_dir(oparent));
	assertion(is_dir(nparent));

	assertion(oname->__getitem__(0) != 0);
	assertion(nname->__getitem__(0) != 0);

	_inode->begin_tx();

	Stat *attr = _inode->get_iattr(oparent);
	assertion(UGE(attr->nlink, 2));
	attr->nlink -= 1;
	_inode->set_iattr(oparent, attr);

	attr = _inode->get_iattr(nparent);
	assertion(ULE(attr->bsize, 522));
	attr->size = Concat32(BitVecVal(522, 32), BitVecVal(4096 * 522, 32));
	assertion(ULT(attr->nlink, attr->nlink + 1));
	attr->nlink += 1;
	_inode->set_iattr(nparent, attr);

	Tuple4 *tp = locate_dentry_ino(oparent, oname);
	Block *oparent_block = tp->get_block();
	uint64_t oparent_bid = tp->get_bid();
	uint64_t ooff = tp->get_off();
	int ovalid = tp->get_valid();

	assertion(ovalid);
	uint64_t ino = oparent_block->__getitem__(ooff);
	clear_dentry(oparent_block, ooff);
	_inode->write(oparent_bid, oparent_block);

	tp = locate_dentry_ino(nparent, nname);
	Block *nparent_block = tp->get_block();
	uint64_t nparent_bid = tp->get_bid();
	uint64_t noff = tp->get_off();
	int nvalid = tp->get_valid();

	if (nvalid) {
		_orphans->append(nparent_block->__getitem__(noff));
		clear_dentry(nparent_block, noff);
	}

	Tuple3 *tp3 = locate_empty_dentry_slot_ino(nparent);
	nparent_block = tp3->get_block();
	nparent_bid = tp3->get_bid();
	noff = tp3->get_off();

	write_dentry(nparent_block, noff, ino, nname);
	_inode->write(nparent_bid, nparent_block);

	_inode->commit_tx();

	return 0;
}

void DirImpl::fsync() {
	_txndisk->flush();
}

void DirImpl::gc1(uint64_t orph_index, uint64_t off) {
	uint64_t ino = Extract(31, 0, _orphans->index(orph_index));
	if (! is_gcable(ino)) {
		return ;
	}
	
	_inode->begin_tx();
	_inode->bunmap(Concat32(ino, off));

	uint64_t nsize = off;

	Stat *attr = _inode->get_iattr(ino);
	if (attr->bsize == nsize + 1) {
		attr->size = Concat32(nsize, nsize * 4096);
		_inode->set_iattr(ino, attr);
	}
	_inode->commit_tx();
}

void DirImpl::gc2(uint64_t orph_index) {
	uint64_t ino = Extract(31, 0, _orphans->index(orph_index));
	if (! is_gcable(ino)) {
		return ;
	}

	if (_inode->get_iattr(ino)->size == 0) {
		_inode->begin_tx();
		_orphans->clear(orph_index);
		_ibitmap->unset_bit(ino);
		_inode->commit_tx();
	}
}

void DirImpl::gc3() {
	_inode->begin_tx();
	_orphans->reset();
	_inode->commit_tx();
}
