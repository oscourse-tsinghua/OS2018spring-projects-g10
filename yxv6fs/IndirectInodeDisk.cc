#include "diskimpl.h"
#include "IndirectInodeDisk.h"

uint64_t IndirectInodeDisk::NINDIRECT = 512;

IndirectInodeDisk::IndirectInodeDisk(InodeDisk *idisk) {
	_NINDIRECT = NINDIRECT;
	_idisk = idisk;
}

void IndirectInodeDisk::begin_tx() {
	_idisk->begin_tx();
}

void IndirectInodeDisk::commit_tx() {
	_idisk->commit_tx();
}

Stat* IndirectInodeDisk::get_iattr(uint64_t ino) {
	return _idisk->get_iattr(ino);
}

void IndirectInodeDisk::set_iattr(uint64_t ino, Stat *attr) {
	_idisk->set_iattr(ino, attr);
}

Block* IndirectInodeDisk::read(uint64_t lbn) {
	return _idisk->read(lbn);
}

void IndirectInodeDisk::write_tx(uint64_t lbn, Block *data) {
	_idisk->write_tx(lbn, data);
}

void IndirectInodeDisk::write(uint64_t lbn, Block *data) {
	_idisk->write_tx(lbn, data);
}

uint64_t IndirectInodeDisk::mappingi(uint64_t vbn) {
	uint64_t ndir = _idisk->_NDIRECT;

	uint64_t ino = Extract(64 - 1, 32, vbn);
	uint64_t off = Extract(32 - 1, 0, vbn);

	int is_direct = ULT(off, ndir);
	off = USub(off, ndir);
	uint64_t vbnm = Concat32(ino, BitVecVal(ndir - 1, 32));

	int ind_mapped = _idisk->is_mapped(vbnm);
	uint64_t ind_mapping = _idisk->mappingi(vbnm);
	Block *ind_block = _idisk->read(ind_mapping);

        return If(is_direct, _idisk->mappingi(vbn), If(And(ULT(off, _NINDIRECT), ind_mapped), ind_block->get(Extract(8, 0, off)), 0));


}

int IndirectInodeDisk::is_mapped(uint64_t vbn) {
	return mappingi(vbn) != 0;
}

int IndirectInodeDisk::is_free(uint64_t lbn) {
	return _idisk->is_free(lbn);
}

uint64_t IndirectInodeDisk::bmap(uint64_t vbn) {
	uint64_t ino = Extract(64 - 1, 32, vbn);
	uint64_t off = Extract(32 - 1, 0, vbn);
	uint64_t eoff = Extract(9 - 1, 0, USub(off, _idisk->_NDIRECT));

	if (ULT(off, _idisk->_NDIRECT)) {
		return _idisk->bmap(vbn);
	}

	if (Not(ULT(off, _idisk->_NDIRECT + _NINDIRECT))) {
		return 0;
	}

	uint64_t mapping = _idisk->bmap(Concat32(ino, BitVecVal(_idisk->_NDIRECT - 1, 32)));
	Block *imap = _idisk->read(mapping);
	uint64_t old_lbn = imap->__getitem__(eoff);

	if (old_lbn == 0) {
		uint64_t lbn = _idisk->alloc();
		write_tx(lbn, ConstBlock(0));
		imap->__setitem__(eoff, lbn);
		write_tx(mapping, imap);
		return lbn;
	}

	return old_lbn;
}

void IndirectInodeDisk::bunmap(uint64_t vbn) {
	uint64_t ino = Extract(64 - 1, 32, vbn);
	uint64_t off = Extract(32 - 1, 0, vbn);
	uint64_t eoff = Extract(9 - 1, 0, USub(vbn, _idisk->_NDIRECT));

	if (Not(ULT(off, _idisk->_NDIRECT + _NINDIRECT))) {
		return ;
	}

	if (ULT(off, _idisk->_NDIRECT)) {
		_idisk->bunmap(vbn);
		return ;
	}

	uint64_t mapping = _idisk->mappingi(Concat32(ino, BitVecVal(_idisk->_NDIRECT - 1, 32))); 
	Block *imap = _idisk->read(mapping);

	if (Or(mapping == 0, imap->__getitem__(eoff) == 0)) {
		return ;
	}

	uint64_t lbn = imap->__getitem__(eoff);
	imap->__setitem__(eoff, 0);

	_idisk->free(lbn);
	write_tx(mapping, imap);
}

