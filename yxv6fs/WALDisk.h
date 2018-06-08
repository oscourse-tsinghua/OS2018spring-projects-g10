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
		TripleList *_txn;
		PartitionAsyncDiskList *_datadisks;
		CacheDict *_cache;

		WALDisk(PartitionAsyncDisk *logdisk, PartitionAsyncDiskList *datadisks, int osync);

		void begin_tx();

		void write_tx(uint64_t dev, uint64_t bid, Block *data);

		void write(uint64_t dev, uint64_t bid, Block *data);

		void flush();

		void commit_tx(int force);

		void writev(TripleList *);

		void __commit();

		Block* read(uint64_t dev, uint64_t bid);

		Block* _read(uint64_t dev, uint64_t bid);

		void __recover();

};

