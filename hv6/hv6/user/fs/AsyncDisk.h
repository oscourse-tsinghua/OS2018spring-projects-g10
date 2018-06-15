#pragma once
#ifndef ASYNCDISK 
#define ASYNCDISK
#ifdef __cplusplus
extern "C" {
    #include "fs.h"
}
#include "Block.h"

extern char _binary_fs_img_start[], _binary_fs_img_end[];

class AsyncDisk {
    public:
        int size;
        int offset;
        AsyncDisk(int _size = 1000, int _offset = 0) {
            size = _size;
            offset = _offset;
            pr_info("fs: use memory based AsyncDisk.\n");
        }
        ~AsyncDisk();
        void write(uint64_t blknum, Block* block, bool cond=1) {
            if(cond) write(blknum, block->buf);
        }
        void write(uint64_t blknum, const void *buf) {
            memcpy(_binary_fs_img_start + offset + blknum * BSIZE, buf, BSIZE);
            // Block* block = (Block*)malloc(sizeof(Block));
            // block->size = BSIZE/sizeof(uint8_t);
            // memcpy(block->buf, ((struct buf*)buf)->data, BSIZE);
            // write(blknum, block);
        }

        Block* read(uint64_t blknum) {
            Block* block = (Block*)malloc(sizeof(Block));
            block->size = BSIZE/sizeof(uint8_t);
            char* buf = (char*)block->buf;
            memcpy(buf, _binary_fs_img_start + offset + blknum * BSIZE, BSIZE);
            read(blknum, block->buf);
            return block;
        }
        void read(uint64_t blknum, void* buf) {
            memcpy(buf, _binary_fs_img_start + offset + blknum * BSIZE, BSIZE);
            // Block* block;
            // read(blknum, block);
            // memcpy(buf, block->buf, BSIZE);
        }

        void flush(void) {
        }
};

#else

typedef struct AsyncDisk AsyncDisk;

#endif



#ifdef __cplusplus
extern "C"
void initAsyncDisk(); 
#endif

#endif
