#pragma once

typedef unsigned long long uint64_t;

inline int Or(int a, int b) {
	return a | b;
}

inline int Extend(uint64_t a, uint64_t b);

inline int ULE(uint64_t a, uint64_t b);
inline int UGE(uint64_t a, uint64_t b);

inline uint64_t BitVecVal(uint64_t val, uint64_t size);

inline uint64_t USub(uint64_t a, uint64_t b) {
	return a - b;
}

inline uint64_t LShR(uint64_t a, uint64_t b) {
	return a >> b;
}

inline uint64_t UGT(uint64_t a, uint64_t b);

inline uint64_t Concat32(uint64_t a, uint64_t b) {
	return (a << 32) | b;
}

inline uint64_t If(int cond, uint64_t a, uint64_t b) {
	if (cond) {
		return a;
	} 
	return b;
}


inline uint64_t Extract(int hi, int lo, uint64_t val) {
    return val >> lo & (((uint64_t)1 << (hi - lo + 1)) - (uint64_t)1);
}

inline int And(int a = 1, int b = 1, int c = 1) {
	return (a && b) && c;
}

inline int ULT(uint64_t a, uint64_t b) {
	return a < b;
}

class Block {
	public:
		void __setitem__(uint64_t key, uint64_t val) {
		}
		uint64_t __getitem__(uint64_t key) {
		}
		void set(uint64_t key, uint64_t val) {
		}
		uint64_t get(uint64_t key);
};

Block *ConstBlock(uint64_t val) {
	return new Block();
}

class PartitionAsyncDisk {
	public:
		void write(uint64_t blknum, Block *block, int cond = 1) {
		}
		Block* read(uint64_t blknum) {
			return new Block();
		}
		void flush() {
		}
};

// class Disk {
// 	public:
// 		void write(uint64_t blknum, Block *block, int cond = 1) {
// 		}
// 		Block* read(uint64_t blknum) {
// 			return new Block();
// 		}
// 		void flush() {
// 		}	
// };

// class Stat {
//     public:
// 		uint64_t size;
//         uint64_t mtime;
//         uint64_t mode;
//         uint64_t nlink;
// 		Stat(uint64_t _size, uint64_t _mtime, uint64_t _mode, uint64_t _nlink) {
// 			size = _size;
// 			mtime = _mtime;
// 			mode = _mode;
// 			nlink = _nlink;
// 		}
// };

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
		Block *get3(uint64_t dev, uint64_t bid, Block *dresult) {
			return dresult;
		}
		void set3(uint64_t dev, uint64_t bid, Block *data) {
		}
};

