#pragma once

#include "diskimpl.h"

typedef unsigned long long uint64_t;

class WALDisk {
	public:
		uint64_t LOG_BID_HEADER_BLOCK;
		uint64_t LOG_DEV_HEADER_BLOCK;
		uint64_t LOG_HEADER_BLOCK;
		uint64_t PER_BLOCK;
		uint64_t LOG_MAX_ENTRIES;

		int _osync;
		PartitionAsyncDisk *_logdisk;
		List *_datadisks;
		List *_txn;
		Dict *_cache;

		void __recover() {
		}

		WALDisk(PartitionAsyncDisk *logdisk, List *datadisks, int osync = true) {
			LOG_MAX_ENTRIES = 10;
			LOG_BID_HEADER_BLOCK = 0;
			LOG_DEV_HEADER_BLOCK = 2;
			LOG_HEADER_BLOCK = 3;

			PER_BLOCK = 511;

			_osync = osync;
			_logdisk = logdisk;
			_datadisks = datadisks;

			__recover();
			_txn = new TripleList();
			_cache = new Dict();
		}

		void begin_tx() {
			if ((! _osync) && _txn->isNotNone()) {
				return ;
			}
			_txn->clear();
			_cache = new Dict();
		}

		void write_tx(uint64_t dev, uint64_t bid, Block *data) {

		}

		void flush() {
		}

		void commit_tx(int force) {
		}

		void writev(List *) {
		}

		void __commit() {
		}

		Block *read(uint64_t dev, uint64_t bid) {
		}
};

