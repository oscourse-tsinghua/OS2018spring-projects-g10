#include "AsyncDisk.h"

extern AsyncDisk defaultAsyncDisk;

extern "C"
void unix_init(void)
{
    pr_info("fs: use memfs\n");
}

extern "C"
void unix_read(uint64_t block, void *buf)
{
    memcpy(buf, _binary_fs_img_start + block * BSIZE, BSIZE);
}

extern "C"
void unix_write(uint64_t block, const void *buf)
{
    memcpy(_binary_fs_img_start + block * BSIZE, buf, BSIZE);
}

extern "C"
void unix_flush(void)
{
}