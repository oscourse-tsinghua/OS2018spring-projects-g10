#pragma once

#include "diskimpl.h"
#include "InodeDisk.h"

typedef unsigned long long uint64_t;

class Partition {
    public:
        uint64_t _start;
        uint64_t _end;
        Disk* _disk;

        Partition(Disk* disk, uint64_t start, uint64_t end) {
            _start = start;
            _end = end;
            _disk = disk;
        }

        bool valid(uint64_t bid) {
            return ULT(bid, _end - _start);
        }

        Block* read(uint64_t bid) {
            return _disk->read(bid + _start);
        }

        void write(uint64_t bid, Block* block) {
            assertion(valid(bid));
            _disk->write(bid + _start, block);
        }

        void flush() {
            _disk->flush();
        }
};