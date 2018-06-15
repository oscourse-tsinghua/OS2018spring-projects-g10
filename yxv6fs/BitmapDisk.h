#pragma once

#include "diskimpl.h"
#include "InodeDisk.h"

typedef unsigned long long uint64_t;

class BitmapDisk {
    public:
        Disk *_disk;
        BitmapDisk(Disk *disk) {
            _disk = disk;
        }
        bool is_set(uint64_t bit) {
            // Define bit as Concat(.., ..)
            uint64_t mapbit = Extract(6 - 1, 0, bit);
            uint64_t mapfield = Extract(6 + 9 - 1, 6, bit);
            uint64_t mapbid = Extract(64 - 1, 6 + 9, bit);
            
            Block* block = _disk->read(mapbid);
            uint64_t field = block->__getitem__(mapfield);
            
            return Extract(0, 0, field >> Extend(mapbit, 64)) == 1;
        }
        
        void set_bit(uint64_t bit){
            uint64_t mapbit = Extract(6 - 1, 0, bit);
            uint64_t mapfield = Extract(6 + 9 - 1, 6, bit);
            uint64_t mapbid = Extract(64 - 1, 6 + 9, bit);

            Block* block = _disk->read(mapbid);

            uint64_t field = block->__getitem__(mapfield);
            uint64_t new_field = field | BitVecVal(1, 64) << Extend(mapbit, 64);

            block->__setitem__(mapfield, new_field);
            _disk->write(mapbid, block);
        }

        void unset_bit(uint64_t bit) {
            uint64_t mapbit = Extract(6 - 1, 0, bit);
            uint64_t mapfield = Extract(6 + 9 - 1, 6, bit);
            uint64_t mapbid = Extract(64 - 1, 6 + 9, bit);

            Block* block = _disk->read(mapbid);

            uint64_t field = block->__getitem__(mapfield);
            uint64_t new_field = field & (~(BitVecVal(1, 64) << Extend(mapbit, 64)));

            block->__setitem__(mapfield, new_field);
            _disk->write(mapbid, block);
        }
};