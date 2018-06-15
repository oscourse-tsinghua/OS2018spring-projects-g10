#pragma once

#include "diskimpl.h"
#include "InodeDisk.h"

typedef unsigned long long uint64_t;

class InodePackDisk {
    public: 
        uint64_t SIZE;
        uint64_t MTIME;
        uint64_t MODE;
        uint64_t NLINK;
        uint64_t _UNUSED;
        uint64_t OFF;
        Disk* _disk;

        InodePackDisk(Disk* metadisk, Disk* datadisk) {
            _disk = metadisk;
            SIZE = 0;
            MTIME = 1;
            MODE = 2;
            NLINK = 3;
            _UNUSED = 4;
            OFF = 5;
        }

        Block* read(uint64_t ino) {
            return _disk->read(LShR(ino, 5));
        }

        void set_iattr(uint64_t ino, Stat attr, Block* block=0) {
            uint64_t off = Extract(8, 0, ino * 16);
            uint64_t bid = LShR(ino, 5);

            Block* inode;
            if(block==0) {
                inode = _disk->read(bid);
            } else {
                inode = block;
            }

            inode->__setitem__(SIZE + off, attr.size);
            inode->__setitem__(MTIME + off, attr.mtime);
            inode->__setitem__(MODE + off, attr.mode);
            inode->__setitem__(NLINK + off, attr.nlink);
            _disk->write(bid, inode);
        }

        Stat* get_iattr(uint64_t ino, Block* block = 0) {
            uint64_t off = Extract(8, 0, ino * 16);
            uint64_t bid = LShR(ino, 5);
            
            Block* inode;
            if(block==0) {
                inode = _disk->read(bid);
            } else {
                inode = block;
            }

            Stat* stat = new Stat(inode->__getitem__(off + SIZE), inode->__getitem__(off + MTIME), inode->__getitem__(off + MODE), inode->__getitem__(off + NLINK));
            return stat;            
        }

        void set_mapping(uint64_t ino, uint64_t off, uint64_t ptr, Block* block = 0) {
            assertion(ULT(off, 11));

            uint64_t ioff = Extract(8, 0, ino * 16);
            uint64_t bid = LShR(ino, 5);
            Block* old;
            if(block==0) {
                old = _disk->read(bid);
            } else old = block;

            old->__setitem__(off + ioff + OFF, ptr);
            _disk->write(bid, old);
        }

        uint64_t get_mapping(uint64_t ino, uint64_t off, Block* block = 0) {
            if(off >= 11) return 0;
            return _get_mapping(ino, off, block);
        }

        uint64_t _get_mapping(uint64_t ino, uint64_t off, Block* block = 0) {
            uint64_t ioff = Extract(8, 0, ino * 16);
            uint64_t bid = LShR(ino, 5);
            if(block==0) {
                block = _disk->read(bid);
            }
            return block->__getitem__(off + ioff + OFF);
        }
};