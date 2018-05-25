#ifndef TRANSACTIONDISK_H
#define TRANSACTIONDISK_H

#include "user.h"
#include "asyncdisk.h"

#define MAX_DATADISK 10
#define MAX_TXN 10

class TransactionDisk {
	public:
		uint64_t LOG_BID_HEADER_BLOCK;
		uint64_t LOG_DEV_HEADER_BLOCK;
		uint64_t LOG_HEADER_BLOCK;
		uint64_t PER_BLOCK;
		int _osync;
		AsyncDisk *_logdisk;
		void* _datadisks[MAX_DATADISK];
		void* _txn[MAX_DATADISK];
		void* _cache;
		int num_datadisks;
		int num_txn;

		TransactionDisk(AsyncDisk *logdisk, void* datadisks, bool osync=true);
		void begin_tx();
		void write_tx(uint64_t dev, uint64_t bid, Block *data);
		void flush();
		void commit_tx(int force);
		void writev(void *);
		void __commit();
		Block* read(uint64_t dev, uint64_t bid);
};

#endif
