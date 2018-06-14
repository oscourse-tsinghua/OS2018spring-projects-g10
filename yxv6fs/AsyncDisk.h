#include "fs.h"
#include "Block.h"

extern char _binary_fs_img_start[], _binary_fs_img_end[];

class AsyncDisk {
    private:
        int size;
        int offset;
    public:
        AsyncDisk(int _size = 1000, int _offset = 0) {
            size = _size;
            offset = _offset;
            pr_info("fs: use memory based AsyncDisk.\n");
        }
        ~AsyncDisk();
        void write(uint64_t blknum, Block block, bool cond=1) {
            memcpy(_binary_fs_img_start + _offset + block * BSIZE, buf, BSIZE);        
        }
        void write(uint64_t blknum, const void *buf) {
            Block block(BSIZE);
            memcpy(block.buf, ((struct buf*)buf)->data, BSIZE);
            write(blknum, block);
        }

        void read(uint64_t blknum, Block* block) {
            block = new Block(BSIZE);
            char* buf = (char*)block->buf;
            memcpy(buf, _binary_fs_img_start + _offset + blknum * BSIZE, BSIZE);
            return block;
        }
        void read(uint64_t blknum, void* buf) {
            Block* block = new Block(BSIZE);
            read(blknum, block);
            memcpy(buf, block->data, BSIZE);
        }

        void flush(void) {
        }
};

AsyncDisk defaultAsyncDisk();