extern "C" {
#include "fs.h"
}
#include "adapt_utils.h"
#include "AsyncDisk.h"

struct logheader {
    int n;
    int sector[LOGSIZE];
};

struct log {
    // struct spinlock lock;
    int start;
    int size;
    int outstanding; // how many FS sys calls are executing.
    int committing;  // in commit(), please wait.
    int dev;
    struct logheader lh;
};

struct log thelog;

extern AsyncDisk* defaultAsyncDisk;

typedef AsyncDisk PartitionAsyncDisk;

class WalDisk {
    private:
    void exclusive_get_superblock() {
        struct superblock sb;
        // initlock(&thelog.lock, "log");
        readsb(ROOTDEV, &sb);
        thelog.start = sb.size - sb.nlog;
        thelog.size = sb.nlog;
        thelog.dev = ROOTDEV;
    }
    // Read the log header from disk into the in-memory log header
    static void exclusive_read_head(void)
    {
        struct buf *b = bread(thelog.dev, thelog.start);
        struct logheader *lh = (struct logheader *)(b->data);
        int i;
        thelog.lh.n = lh->n;
        for (i = 0; i < thelog.lh.n; i++) {
            thelog.lh.sector[i] = lh->sector[i];
        }
        brelse(b);
    }
    // Copy committed blocks from log to their home location
    static void exclusive_install_trans(void)
    {
        int tail;

        for (tail = 0; tail < thelog.lh.n; tail++) {
            struct buf *lbuf = bread(thelog.dev, thelog.start + tail + 1); // read log block
            struct buf *dbuf = bread(thelog.dev, thelog.lh.sector[tail]);  // read dst
            memmove(dbuf->data, lbuf->data, BSIZE);                        // copy block to dst
            bwrite(dbuf);                                                  // write dst to disk
            brelse(lbuf);
            brelse(dbuf);
        }
    }

    static void exclusive_write_zero(void) {
        thelog.lh.n = 0;
        write_head(); // clear the log
    }
    public:
    uint64_t LOG_BID_HEADER_BLOCK;
    uint64_t LOG_DEV_HEADER_BLOCK;
    uint64_t LOG_HEADER_BLOCK;
    uint64_t PER_BLOCK;
    uint64_t LOG_MAX_ENTRIES;

    uint64_t _osync;

    PartitionAsyncDisk *_logdisk;
    TripleList *_txn;
    PartitionAsyncDiskList *_datadisks;
    CacheDict *_cache;
    
    void __init__(PartitionAsyncDisk* logdisk, PartitionAsyncDiskList* datadisks, uint64_t osync=1)
    {
        // if (sizeof(struct logheader) >= BSIZE)
        //     panic("initlog: too big logheader");

        LOG_BID_HEADER_BLOCK = 0;
        LOG_DEV_HEADER_BLOCK = 2;
        LOG_HEADER_BLOCK = 3;
        LOG_MAX_ENTRIES = 10;
        
        PER_BLOCK = 511;

        _osync = osync;
        _logdisk = logdisk;
        _datadisks = datadisks;

        exclusive_get_superblock();
        __recover();
        
        _txn = (TripleList*) malloc(sizeof(TripleList));
        _cache = (CacheDict*) malloc(sizeof(CacheDict));
    }

    // Write in-memory log header to disk.
    // This is the true point at which the
    // current transaction commits.
    static void write_head(void)
    {
        ideflush(); // flush all preceding writes to disk
        struct buf *buf = bread(thelog.dev, thelog.start);
        struct logheader *hb = (struct logheader *)(buf->data);
        int i;
        hb->n = thelog.lh.n;
        for (i = 0; i < thelog.lh.n; i++) {
            hb->sector[i] = thelog.lh.sector[i];
        }
        bwrite(buf);
        ideflush(); // flush head
        brelse(buf);
    }

    void __commit() {
        for (uint64_t k = 0; k < _datadisks->__len__(); ++ k) {
		    _datadisks->__getitem__(k)->flush();
        }
        Block *hdr = ConstBlock(0);
        _logdisk->write(LOG_BID_HEADER_BLOCK, hdr, AND(1, 1));
        _logdisk->flush();

        exclusive_write_zero();
        
    }

    void __recover(void)
    {
        Block *hdr_bid1 = _logdisk->read(LOG_BID_HEADER_BLOCK);
        Block *hdr_dev1 = _logdisk->read(LOG_DEV_HEADER_BLOCK);
        Block *hdr_bid2 = _logdisk->read(LOG_BID_HEADER_BLOCK + 1);
        Block *hdr_dev2 = _logdisk->read(LOG_DEV_HEADER_BLOCK + 1);
        uint64_t n = hdr_bid1->__getitem__(0);
        exclusive_read_head();
        for (uint64_t i = 0; i < LOG_MAX_ENTRIES; ++ i) {
            uint64_t dev = 0;
            uint64_t bid = 0;
            if (i < PER_BLOCK) {
                dev = hdr_dev1->__getitem__(1 + i);
                bid = hdr_bid1->__getitem__(1 + i);
            } else {
                dev = hdr_dev2->__getitem__(i - PER_BLOCK);
                bid = hdr_bid2->__getitem__(i - PER_BLOCK);
            }
            Block *data = _logdisk->read(LOG_HEADER_BLOCK + i + 1);
            for (uint64_t k = 0; k < _datadisks->__len__(); ++ k) {
                _datadisks->__getitem__(k)->write(bid, data, AND(dev == k, ULT(i, n)));
            }
	    }
        exclusive_install_trans(); // if committed, copy from log to disk
    }

    // called at the start of each FS system call.
    void begin_op(void)
    {
        // acquire(&thelog.lock);
        while (1) {
            if (thelog.committing) {
                // sleep(&thelog, &thelog.lock);
            } else if (thelog.lh.n + (thelog.outstanding + 1) * MAXOPBLOCKS > LOGSIZE) {
                // this op might exhaust log space; wait for commit.
                // sleep(&thelog, &thelog.lock);
            } else {
                thelog.outstanding += 1;
                // release(&thelog.lock);
                break;
            }
        }
    }

    // called at the end of each FS system call.
    // commits if this was the last outstanding operation.
    void end_op(void)
    {
        int do_commit = 0;

        // acquire(&thelog.lock);
        thelog.outstanding -= 1;
        if (thelog.committing)
            // panic("thelog.committing");
        if (thelog.outstanding == 0) {
            do_commit = 1;
            thelog.committing = 1;
        } else {
            // begin_op() may be waiting for log space.
            // wakeup(&thelog);
        }
        // release(&thelog.lock);

        if (do_commit) {
            // call commit w/o holding locks, since not allowed
            // to sleep with locks.
            commit();
            // acquire(&thelog.lock);
            thelog.committing = 0;
            // wakeup(&thelog);
            // release(&thelog.lock);
        }
    }

    // Copy modified blocks from cache to thelog.
    static void write_log(void)
    {
        int tail;

        for (tail = 0; tail < thelog.lh.n; tail++) {
            struct buf *to = bread(thelog.dev, thelog.start + tail + 1);  // log block
            struct buf *from = bread(thelog.dev, thelog.lh.sector[tail]); // cache block
            memmove(to->data, from->data, BSIZE);
            bwrite(to); // write the log
            brelse(from);
            brelse(to);
        }
    }

    static void commit()
    {
        if (thelog.lh.n > 0) {
            write_log();     // Write modified blocks from cache to log
            write_head();    // Write header to disk -- the real commit
            exclusive_install_trans(); // Now install writes to home locations
            thelog.lh.n = 0;
            write_head(); // Erase the transaction from the log
        }
    }

    // Caller has modified b->data and is done with the buffer.
    // Record the block number and pin in the cache with B_DIRTY.
    // commit()/write_log() will do the disk write.
    //
    // log_write() replaces bwrite(); a typical use is:
    //   bp = bread(...)
    //   modify bp->data[]
    //   log_write(bp)
    //   brelse(bp)
    void log_write(struct buf *b)
    {
        int i;

        // if (thelog.lh.n >= LOGSIZE || thelog.lh.n >= thelog.size - 1)
            // panic("too big a transaction");
        // if (thelog.outstanding < 1)
            // panic("log_write outside of trans");

        for (i = 0; i < thelog.lh.n; i++) {
            if (thelog.lh.sector[i] == b->sector) // log absorbtion
                break;
        }
        thelog.lh.sector[i] = b->sector;
        if (i == thelog.lh.n)
            thelog.lh.n++;
        b->flags |= B_DIRTY; // prevent eviction
    }
};

WalDisk walDisk;

extern "C" {
void initlog(void) {
    PartitionAsyncDisk* logdisk;
    PartitionAsyncDiskList* datadisks;
    walDisk.__init__(logdisk, datadisks);
}
void log_write(struct buf * buf) {
    walDisk.log_write(buf);
}
void begin_op() {
    walDisk.begin_op();
}
void end_op() {
    walDisk.end_op();
}
}