#pragma once

#include "diskimpl.h"
#include "WALDisk.h"
#include "InodeDisk.h"
#include "IndirectInodeDisk.h"

class DirLookup {
};

class Allocator32 {
	public:
		Allocator32(Disk *_disk, uint64_t _start, uint64_t _end);
		uint64_t alloc();
};

class Orphans {
	public:
		Disk *_orphandisk;

		Orphans(Disk *orphandisk) {
			_orphandisk = orphandisk;
		}

		uint64_t size() {
			return _orphandisk->read(0)->__getitem__(0);
		}

		uint64_t index(uint64_t idx) {
			Block *orphanblock = _orphandisk->read(0);
			uint64_t n = orphanblock->__getitem__(0);
			assertion(0 <= n);
			assertion(n < 511);
			uint64_t np = Extract(8, 0, idx);
			return orphanblock->__getitem__(np + 1);
		}

		void reset() {
			_orphandisk->write(0, ConstBlock(0));
		}

		void clear(uint64_t idx) {
			Block *orphanblock = _orphandisk->read(0);
			uint64_t np = Extract(8, 0, idx);
			orphanblock->__setitem__(np, 0);
			_orphandisk->write(0, orphanblock);
		}

		void append(uint64_t value) {
			Block *orphanblock = _orphandisk->read(0);
			uint64_t n = orphanblock->__getitem__(0);
			assertion(0 <= n);
			assertion(n < 511);
			uint64_t np = Extract(8, 0, n);
			orphanblock->__setitem__(np + 1, value);
			orphanblock->__setitem__(0, n + 1);
			_orphandisk->write(0, orphanblock);
		}

};

class MyPIno {
	public: 
		IndirectInodeDisk *inode;

		MyPIno(IndirectInodeDisk *_inode) {
			inode = _inode;
		}

		int is_mapped(uint64_t vbn, IndirectInodeDisk *_inode = 0) {
			if (_inode == 0) {
				return inode->is_mapped(vbn);
			}
			return _inode->is_mapped(vbn);
		}

		uint64_t mappingi(uint64_t vbn, IndirectInodeDisk *_inode = 0) {
			if (_inode == 0) {
				return inode->mappingi(vbn);
			}
			return _inode->mappingi(vbn);
		}

		Block *read(uint64_t bid, IndirectInodeDisk *_inode = 0) {
			if (_inode == 0) {
				return inode->read(bid);
			}
			return _inode->read(bid);
		}

		uint64_t bmap(uint64_t bid, IndirectInodeDisk *_inode = 0) {
			if (_inode == 0) {
				return inode->bmap(bid);
			}
			return _inode->bmap(bid);
		}

};

class DirImpl {
	public:
		WALDisk *_txndisk;
		IndirectInodeDisk *_inode;

		Allocator32 *_iallocator;
		Disk *_ifree;

		Bitmap *_ibitmap;

		DirLookup *_dirloop;

		Disk *_orphans;
};
