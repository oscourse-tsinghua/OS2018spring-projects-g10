#ifndef DISKIMPL
#define DISKIMPL

#include "user.h"

inline uint64_t Extract(int hi, int lo, uint64_t val) {
	return val >> lo & (((uint64_t)1 << (hi - lo + 1)) - (uint64_t)1);
}

inline uint64_t USub(uint64_t a, uint64_t b) {
	return a - b;
}

inline uint64_t Concat32(uint64_t a, uint64_t b) {
	return a << 32 | b;
}

inline int ULE(uint64_t a, uint64_t b) {
	return a <= b;
}

inline int ULT(uint64_t a, uint64_t b) {
	return a < b;
}

inline int UGE(uint64_t a, uint64_t b) {
	return a >= b;
}

inline int UGT(uint64_t a, uint64_t b) {
	return a > b;
}

inline uint64_t URem(uint64_t a, uint64_t b) {
	return a % b;
}

inline uint64_t UDiv(uint64_t a, uint64_t b) {
	return a / b;
}

inline uint64_t LShR(uint64_t a, uint64_t b) {
	return a >> b;
}

inline uint64_t Extend(uint64_t val, uint64_t size) {
	assert(size == 64, "");
	return val;
}

inline uint64_t BitVecVal(uint64_t val, uint64_t size) {
	assert(size <= 64, "");
	return val;
}

inline int Not(int cond) {
	return not cond;
}

inline int Or(int a, int b) {
	return (a or b);
}

inline int And(int a, int b, int c);
Block ConstBlock(uint64_t c);

// inline If()

void assertion(int b, char *msg);

struct Stat {
	uint64_t size, mtime, mode, nlink;
};

struct Block {
	uint64_t *buf;
	int size;
	struct Block* (*copy)(struct Block*);
	void (*set)(struct Block*, uint64_t, uint64_t);
	void (*get)(struct Block*, uint64_t);
};

struct AsyncDisk {
	char *fn;
	int fd;
	void (*write)(struct AsyncDisk*, uint64_t, struct Block*, int);
	struct Block* (read*)(struct AsyncDisk*, uint64_t);
	void (flush*)(struct AsyncDisk*);
};

struct Dict {
	struct dict *_map;
	void get(struct Dict*, int, int);
	void has_key(struct Dict*, int);
};

struct PartitionAsyncDisk {
	struct AsyncDisk *adisk;
	uint64_t start, end;
	int debug;
	void (write*)(struct PartitionAsyncDisk*, uint64_t, struct Block*, int);
	struct Block* (read*)(struct PartitionAsyncDisk*, uint64_t);
	void (flush*)(struct PartitionAsyncDisk*);
};

struct Allocator {
	void *readfn;
	uint64_t start, end;
	uint64_t (_alloc*)(struct Allocator*, uint64_t, struct Block*);
	uint64_t (alloc*)(struct Allocator*);
};

struct DentryLookup {
};

#endif
