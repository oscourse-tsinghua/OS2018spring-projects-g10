#pragma once

#include "diskimpl.h"
#include "WALDisk.h"
#include "InodeDisk.h"
#include "IndirectInodeDisk.h"

class errno {
	public:
		static uint64_t ENOSPC;
		static uint64_t ENOENT;
		static uint64_t ENOTDIR;
};

uint64_t errno::ENOSPC;
uint64_t errno::ENOENT;
uint64_t errno::ENOTDIR;

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

class Tuple2 {
	public:
		Tuple2(uint64_t _a, uint64_t _b);
		uint64_t __getitem__(uint64_t idx);
};

class Tuple3 {
	public:
		Tuple3(Block *block, uint64_t _bid, uint64_t _off);
		uint64_t get_bid();
		uint64_t get_off();
		Block *get_block();
};

class Tuple4 {
	public:
		Tuple4(Block *block, uint64_t _bid, uint64_t _off, int _valid);
		uint64_t get_bid();
		uint64_t get_off();
		Block *get_block();
		int get_valid();
};

class NameType {
	public:
		uint64_t __getitem__(uint64_t idx);
};

class DirLook {
	public:
		DirLook(MyPIno *pino);
		Tuple2* locate_dentry_ino(uint64_t ino, NameType *name);
		Tuple2* locate_empty_slot_ino(uint64_t ino);
};

class DirImpl {
	public:
		static uint64_t NBLOCKS;
		static uint64_t IFREEDISK;
		static uint64_t ORPHANS;

		WALDisk *_txndisk;
		IndirectInodeDisk *_inode;

		Allocator32 *_iallocator;
		Disk *_ifree;

		Bitmap *_ibitmap;

		DirLook *_dirlook;

		Orphans *_orphans;

		DirImpl(WALDisk *txndisk, IndirectInodeDisk *inode);
		Tuple4 *locate_dentry_ino(uint64_t ino, NameType *name);
		Tuple3 *locate_empty_dentry_slot_ino(uint64_t ino);
		Tuple4 *locate_empty_dentry_slot_err_ino(uint64_t ino);
		void write_dentry(Block *block, uint64_t off, uint64_t ino, NameType *name);
		void clear_dentry(Block *block, uint64_t off);
		uint64_t ialloc();
		int is_ifree(uint64_t ino);
		int is_valid(uint64_t ino);
		int is_gcable(uint64_t ino);
		int is_dir(uint64_t ino);
		int is_regular(uint64_t ino);
		Stat *get_iattr(uint64_t ino);
		void set_iattr(uint64_t ino, Stat *attr);
		Block* read(uint64_t ino, uint64_t blocknum);
		void truncate(uint64_t ino, uint64_t fsize);
		uint64_t write(uint64_t ino, uint64_t blocknum, Block *v, uint64_t size = BitVecVal(4096, 32));
		uint64_t lookup(uint64_t parent, NameType *name);
		Tuple2 *mknod(uint64_t parent, NameType *name, uint64_t mode, uint64_t mtime);
		uint64_t unlink(uint64_t parent, NameType *name);
		Tuple2 *rmdir(uint64_t parent, NameType *name);
		uint64_t rename(uint64_t oparent, NameType *oname, uint64_t nparent, NameType *nname);
		void forget(uint64_t ino);
		void fsync();
		void gc1(uint64_t orph_index, uint64_t off);
		void gc2(uint64_t orph_index);
		void gc3();
};
