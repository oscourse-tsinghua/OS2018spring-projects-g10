#pragma once

#include "diskimpl.h"
#include "WALDisk.h"
#include "InodeDisk.h"

class IndirectInodeDisk {
	public:
		static uint64_t NINDIRECT;
		uint64_t _NINDIRECT;
		InodeDisk *_idisk;

		IndirectInodeDisk(InodeDisk *idisk);

		void begin_tx();
		void commit_tx();

		Stat *get_iattr(uint64_t ino);
		void set_iattr(uint64_t ino, Stat *attr);

		Block *read(uint64_t lbn);
		void write_tx(uint64_t lbn, Block *data);
		void write(uint64_t lbn, Block *data);

		uint64_t mappingi(uint64_t vbn);
		int is_mapped(uint64_t vbn);
		int is_free(uint64_t vbn);
		uint64_t bmap(uint64_t vbn);
		void bunmap(uint64_t vbn);
};


