#include "InodeDisk.h"

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

/*


uint64_t mappingi(uint64_t vbn);
int is_mapped(uint64_t vbn);
int is_free(uint64_t vbn);
uint64_t alloc();
void free(uint64_t lbn);
uint64_t bmap(uint64_t vbn);
void bunmap(uint64_t vbn);
*/
