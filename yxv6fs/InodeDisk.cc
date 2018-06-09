#include "InodeDisk.h"
#include "diskimpl.h"

uint64_t InodeDisk::FREEDISK = 0;
uint64_t InodeDisk::INODEMETADISK = 1;
uint64_t InodeDisk::INODEDATADISK = 2;
uint64_t InodeDisk::DATADISK = 3;
uint64_t InodeDisk::NDIRECT = 11;

InodeDisk::InodeDisk(WALDisk *txndisk) {
	_INODEDATADISK = INODEDATADISK;
	_NDIRECT = NDIRECT;
	_txndisk = txndisk;
	_allocator = new Allocator64(_txndisk, FREEDISK, 0, 1024);
	Disk *freedisk = new Disk(FREEDISK, _txndisk);
	Disk *inodemeta = new Disk(INODEMETADISK, _txndisk);
	Disk *inodedata = new Disk(INODEDATADISK, _txndisk);

	_bitmap = new Bitmap(freedisk);
	_inode = new InodePack(inodemeta, inodedata);
}

Stat* InodeDisk::get_iattr(uint64_t ino) {
	return _inode->get_iattr(ino);
}

void InodeDisk::set_iattr(uint64_t ino, Stat *attr) {
	_inode->set_iattr(ino, attr);
}

void InodeDisk::begin_tx() {
	_txndisk->begin_tx();
}

void InodeDisk::commit_tx() {
	_txndisk->commit_tx();
}

Block* InodeDisk::read(uint64_t lbn) {
	return _txndisk->read(DATADISK, lbn);
}

void InodeDisk::write_tx(uint64_t lbn, Block *data) {
	_txndisk->write_tx(DATADISK, lbn, data);
}

void InodeDisk::write(uint64_t lbn, Block *data) {
	_txndisk->write_tx(DATADISK, lbn, data);
}

uint64_t InodeDisk::mappingi(uint64_t vbn) {
	uint64_t ino = Extract(64 - 1, 32, vbn);
	uint64_t off = Extract(32 - 1, 0, vbn);
	uint64_t eoff = Extract(9 - 1, 0, vbn);
	return If(ULT(off, _NDIRECT), _inode->get_mapping(ino, eoff), 0);
}

int InodeDisk::is_mapped(uint64_t vbn) {
	return mappingi(vbn) != 0;
}

int InodeDisk::is_free(uint64_t lbn) {
	return Not(_bitmap->is_set(lbn));
}

uint64_t InodeDisk::alloc() {
	uint64_t lbn = _allocator->alloc();
        assertion(lbn != 0);
        assertion(is_free(lbn));
	_bitmap->set_bit(lbn);
	return lbn;
}

void InodeDisk::free(uint64_t lbn) {
	return _bitmap->unset_bit(lbn);
}

uint64_t InodeDisk::bmap(uint64_t vbn) {
	uint64_t ino = Extract(64 - 1, 32, vbn);
        uint64_t off = Extract(32 - 1, 0, vbn);
        uint64_t eoff = Extract(9 - 1, 0, vbn);
	Block *iblock = _inode->read(ino);
	uint64_t old_lbn = _inode->get_mapping(ino, eoff, iblock);
	int valid = And(old_lbn == 0, ULT(off, _NDIRECT));
	if (valid) {
		uint64_t lbn = alloc();
		write_tx(lbn, ConstBlock(0));
		_inode->set_mapping(ino, eoff, lbn, iblock);
		return lbn;
	}
	if (ULT(off, _NDIRECT)) {
		return old_lbn;
	}
	return 0;
}

void InodeDisk::bunmap(uint64_t vbn) {
	uint64_t ino = Extract(64 - 1, 32, vbn);
	uint64_t off = Extract(32 - 1, 0, vbn);
	uint64_t eoff = Extract(9 - 1, 0, vbn);
	if (Not(ULT(off, _NDIRECT))) {
		return ;
	}
	Block *iblock = _inode->read(ino);
	uint64_t lbn = _inode->get_mapping(ino, eoff, iblock);

	if (lbn != 0) {
		free(lbn);
		_inode->set_mapping(ino, eoff, 0, iblock);
	}
}

void InodeDisk::mkfs() {
	_bitmap->mkfs();
	_inode->mkfs();
}
