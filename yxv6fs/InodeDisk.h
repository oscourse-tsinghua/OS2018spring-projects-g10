#pragma once

#include "diskimpl.h"
#include "WALDisk.h"

void assertion(int cond, char *msg = 0);

class Disk {
	public:
		Disk(uint64_t _dev, WALDisk *_txndisk);
		Block *read(uint64_t bid);
		void write(uint64_t bid, Block *data);
};

class Allocator64 {
	public:
		Allocator64(WALDisk *_txndisk, uint64_t _dev, uint64_t _start, uint64_t _end);
		uint64_t alloc();
};

class Bitmap {
	public:
		Bitmap(Disk *_disk);
		int is_set(uint64_t lbn);
		void set_bit(uint64_t lbn);
		void unset_bit(uint64_t lbn);
		void mkfs();
};

class Stat {
	public:
		Stat(uint64_t size, uint64_t mtime, uint64_t mode, uint64_t nlink);
		uint64_t nlink;
		uint64_t mode;
		uint64_t bsize;
		uint64_t size;
		uint64_t fsize;
};

class InodePack {
	public:
		InodePack(Disk *_inodemeta, Disk *inodedata);
		Stat *get_iattr(uint64_t ino);
		void set_iattr(uint64_t ino, Stat *attr);
		uint64_t get_mapping(uint64_t ino, uint64_t eoff, Block *block = 0);

		void set_mapping(uint64_t ino, uint64_t off, uint64_t ptr, Block *block = 0);
		Block *read(uint64_t ino);
		void mkfs();
};

class InodeDisk {
	public:
		static uint64_t FREEDISK;
		static uint64_t INODEMETADISK;
		static uint64_t INODEDATADISK;
		static uint64_t DATADISK;
		static uint64_t NDIRECT;

		uint64_t _INODEDATADISK;
		uint64_t _NDIRECT;

		InodeDisk(WALDisk *txndisk);

		WALDisk *_txndisk;
		Allocator64 *_allocator;
		Bitmap *_bitmap;
		InodePack *_inode;

		void begin_tx();
		void commit_tx();

		Stat* get_iattr(uint64_t ino);
		void set_iattr(uint64_t ino, Stat *attr);

		Block* read(uint64_t lbn);
		void write_tx(uint64_t lbn, Block *data);
		void write(uint64_t lbn, Block *data);
		uint64_t mappingi(uint64_t vbn);
		int is_mapped(uint64_t vbn);
		int is_free(uint64_t vbn);
		uint64_t alloc();
		void free(uint64_t lbn);
		uint64_t bmap(uint64_t vbn);
		void bunmap(uint64_t vbn);
		void mkfs();
};
