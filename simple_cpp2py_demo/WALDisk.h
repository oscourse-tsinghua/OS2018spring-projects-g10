#ifndef WALDISK_H
#define WALDISK_H

typedef unsigned long long uint64_t;

class Block {
};

class List {
	public:
		void clear() {
		}
		void append(uint64_t dev,uint64_t bid, Block* data) {
		}
		int length() {
			return 10;
		}
};

class Dict {
	public:
		void set(uint64_t dev,uint64_t bid, Block* data) {
		}
};

class PartitionAsyncDisk {
	public:
		void test_fun() {
		}
		void write(uint64_t bid, Block* data) {
		}
};

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

		WALDisk(PartitionAsyncDisk *logdisk, List *datadisks, int osync=true) {
			LOG_MAX_ENTRIES = 10;
			LOG_BID_HEADER_BLOCK = 0;
			LOG_DEV_HEADER_BLOCK = 2;
			LOG_HEADER_BLOCK = 3;
			PER_BLOCK = 511;
			_osync = osync;
			_logdisk = logdisk;
			_datadisks = datadisks;
			__recover();
			_txn = 0;
			_cache = new Dict();
		}

		void begin_tx() {
			if ((! _osync) && (_txn)) {
				return ;
			}
			_txn->clear();
			_cache = new Dict();
		}

		void write_tx(uint64_t dev, uint64_t bid, Block *data) {
			_txn->append(dev, bid, data);
			_logdisk->write(LOG_HEADER_BLOCK + _txn->length(), data);
			_cache->set(dev, bid, data);
		}

		void __recover() {
		}
};

#endif
