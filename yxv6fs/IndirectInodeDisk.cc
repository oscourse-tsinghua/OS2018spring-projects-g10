#include "diskimpl.h"
#include "IndirectInodeDisk.h"

uint64_t IndirectInodeDisk::NINDIRECT = 512;

IndirectInodeDisk::IndirectInodeDisk(InodeDisk *idisk) {
	_NINDIRECT = NINDIRECT;
	_idisk = idisk;
}

void IndirectInodeDisk::begin_tx() {
	_idisk->commit_tx();
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
	_idisk->read(lbn);
}

void IndirectInodeDisk::write_tx(uint64_t lbn, Block *data) {
	_idisk->write_tx(lbn, data);
}

void IndirectInodeDisk::write(uint64_t lbn, Block *data) {
	_idisk->write_tx(lbn, data);
}

uint64_t IndirectInodeDisk::mappingi(uint64_t vbn) {
	uint64_t ndir = _idisk._NDIRECT;

	uint64_t ino = Extract(64 - 1, 32, vbn);
	uint64_t off = Extract(32 - 1, 0, vbn);

	int is_direct = ULT(off, ndir);
	uint64_t off = USub(off, ndir);
	uint64_t vbnm = Concat32(ino, BitVecVal(ndir - 1, 32));

	int ind_mapped = _idisk.is_mapped(vbnm);
	uint64_t ind_mapping = _idisk.mappingi(vbnm);
	Block *ind_block = _idisk.read(ind_mapping);

        return If(is_direct, _idisk->mappingi(vbn), If(And(ULT(off, _NINDIRECT), ind_mapped), ind_block->get(Extract(8, 0, off)), 0));


}

int IndirectInodeDisk::is_mapped(uint64_t vbn);
int IndirectInodeDisk::is_free(uint64_t vbn);

/*
uint64_t bmap(uint64_t vbn);
void bunmap(uint64_t vbn);

*/
