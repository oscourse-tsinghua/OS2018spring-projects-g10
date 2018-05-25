#include "fs.h"

struct asyncdisk_buf {
}; 

uint8_t* get_asyncdisk_buffer();

void iderw(struct buf *b)
{
    if (!(b->flags & B_BUSY))
        panic("iderw: buf not busy");
    if ((b->flags & (B_VALID | B_DIRTY)) == B_VALID)
        panic("iderw: nothing to do");

    if (b->flags & B_DIRTY) {
        unix_write(b->sector, b->data);
        b->flags &= ~B_DIRTY;
    } else {
        unix_read(b->sector, b->data);
        b->flags |= B_VALID;
    }
}

void ideflush()
{
    unix_flush();
}

// Asyndisk Layer

uint8_t* asyncdisk_read(uint bid) {
	uint8_t *buf = get_asyncdisk_buffer();
	unix_read(bid, buf);
	return buf;
}

void asyncdisk_write(uint bid, uint8_t *data) {
	unix_write(bid, data);
}

void asyncdisk_flush() {
	unix_flush();
}
