#include "WALDisk.h"

WALDisk::WALDisk(PartitionAsyncDisk *logdisk, List *datadisks, int osync = true) {
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

void WALDisk::begin_tx() {
	if ((! _osync) && _txn->isNotNone()) {
		return ;
	}
	_txn->clear();
	_cache = new Dict();
}

void WALDisk::write_tx(uint64_t dev, uint64_t bid, Block *data) {
}

void write(uint64_t dev, uint64_t bid, Block *data);

void flush();

void commit_tx(int force);

void writev(TripleList *);

void __commit();

Block* read(uint64_t dev, uint64_t bid);

Block* _read(uint64_t dev, uint64_t bid);

void __recover();

