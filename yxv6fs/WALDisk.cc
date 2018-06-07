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

