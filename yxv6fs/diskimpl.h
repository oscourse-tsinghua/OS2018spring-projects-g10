#pragma once

typedef unsigned long long uint64_t;

class PartitionAsyncDisk {
};

/*
class List {
	public:
		bool _is_none;
		List() {
			_is_none = true;
		}
		void setNone(bool is_none) {
			_is_none = is_none;
		}
		bool isNone() {
			return _is_none;
		}
		bool isNotNone() {
			return !_is_none;
		}
		void clear() {
			_is_none = false;
		}
};

class TripleList: public List{
};

class PartitionAsyncDiskList: public List{
};

class Dict {
};
*/

class PartitionAsyncDiskList {
	public:
		uint64_t __len__() {
			return 10;
		}
		PartitionAsyncDisk* __getitem__(uint64_t key) {
			return new PartitionAsyncDisk();
		}
};

class TripleList {
	public:
		void setNone(bool _is_none) {
		}
		bool isNone() {
		}
		bool isNotNone() {
		}
		void clear() {
		}
		uint64_t length() {
			return 10;
		}
		void append_triple(uint64_t dev, uint64_t bid, Block *data) {
		}
		uint64_t get_dev(uint64_t idx) {
		}
		uint64_t get_bid(uint64_t idx) {
		}
		Block* get_data(uint64_t idx) {
		}
		TripleList *copy() {
		}
		uint64_t __len__() {
			return 10;
		}
};

class CacheDict {
	public:
		Block *get3(uint64_t dev, uint64_t bid, BLock *dresult) {
			return dresult;
		}
		void set3(uint64_t dev, uint64_t bid, Block *data) {
		}
};

class Block {
};
