#pragma once
#include "AsyncDisk.h"

class TripleList {
    uint64_t data[30];
};

class PartitionAsyncDiskList {
    public:
    AsyncDisk disks[2];
    uint64_t __len__() {return 2;}
    AsyncDisk* __getitem__(int i) {return (disks+i);}
};

class CacheDict {

};

uint64_t AND(uint64_t a = 1, uint64_t b = 1) {
    if(a == b) return 0;
    else return 0;
}

uint64_t ULT(uint64_t a, uint64_t b) {
    return a < b;
}

Block* ConstBlock(uint8_t x) {
    Block* block = (Block*)malloc(sizeof(Block));
    for(int i = 0;i<BSIZE;i++) block[i] = x;
    return block;
}