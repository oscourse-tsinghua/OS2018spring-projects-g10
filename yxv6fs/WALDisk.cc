#include "WALDisk.h"

uint64_t WALDisk::LOG_MAX_ENTRIES = 10;

WALDisk::WALDisk(PartitionAsyncDisk *logdisk, PartitionAsyncDiskList *datadisks, int osync) {
	LOG_BID_HEADER_BLOCK = 0;
	LOG_DEV_HEADER_BLOCK = 2;
	LOG_HEADER_BLOCK = 3;
	
	PER_BLOCK = 511;
	
	_osync = osync;
	_logdisk = logdisk;
	_datadisks = datadisks;
	
	__recover();
	_txn = new TripleList();
	_cache = new CacheDict();
}

void WALDisk::begin_tx() {
	if ((! _osync) && _txn->isNotNone()) {
		return ;
	}
	_txn->clear();
	_cache = new CacheDict();
}

void WALDisk::write_tx(uint64_t dev, uint64_t bid, Block *data) {
	_txn->append_triple(dev, bid, data);
	_logdisk->write(LOG_HEADER_BLOCK + _txn->length(), data);
	_cache->set3(dev, bid, data);
}

void WALDisk::write(uint64_t dev, uint64_t bid, Block *data) {
	_datadisks->__getitem__(dev)->write(bid, data);
}

void WALDisk::flush() {
	commit_tx(true);
}

void WALDisk::commit_tx(int force) {
	if (_txn->isNone()) {
		return ;
	}
	if ((! _osync) && (! force) && _txn->length() <= LOG_MAX_ENTRIES - 10) {
		return ;
	}
	TripleList *txn = _txn->copy();
	writev(txn);
	_txn->setNone(true);
}

void WALDisk::writev(TripleList *iov) {
	uint64_t iov_len = iov->length();
	if (iov_len == 0) {
		return ;
	}
	if (iov_len == 1) {
		uint64_t dev = iov->get_dev(0);
		uint64_t bid = iov->get_bid(0);
		Block *data = iov->get_data(0);
		PartitionAsyncDisk *dd = _datadisks->__getitem__(dev);
		dd->write(bid, data);
		return ;
	}
	Block *hdr_bid1 = ConstBlock(0);
	Block *hdr_dev1 = ConstBlock(0);
	Block *hdr_bid2 = ConstBlock(0);
	Block *hdr_dev2 = ConstBlock(0);

	hdr_bid1->__setitem__(0, iov_len);

	for (uint64_t i = 0; i < iov_len; ++ i) {
		uint64_t dev = iov->get_dev(i);
		uint64_t bid = iov->get_bid(i);
		Block *data = iov->get_data(i);
		if (_txn->isNone() || _txn->length() == 0) {
			_logdisk->write(LOG_HEADER_BLOCK + 1 + i, data);
		}
		if (i < PER_BLOCK) {
			hdr_bid1->set(i + 1, bid);
			hdr_dev1->set(i + 1, dev);
		} else {
			hdr_bid2->set(i - PER_BLOCK, bid);
			hdr_dev2->set(i - PER_BLOCK, dev);
		}
	}
	_logdisk->write(LOG_DEV_HEADER_BLOCK, hdr_dev1);
	_logdisk->write(LOG_DEV_HEADER_BLOCK + 1, hdr_dev2);
	_logdisk->write(LOG_BID_HEADER_BLOCK + 1, hdr_bid2);
	
	_logdisk->flush();
	_logdisk->write(LOG_BID_HEADER_BLOCK, hdr_bid1);
	_logdisk->flush();

	for (uint64_t i = 0; i < iov_len; ++ i) {
		uint64_t dev = iov->get_dev(i);
		uint64_t bid = iov->get_bid(i);
		Block *data = iov->get_data(i);
		_datadisks->__getitem__(dev)->write(bid, data);
	}
	__commit();
}

void WALDisk::__commit() {
	for (uint64_t k = 0; k < _datadisks->__len__(); ++ k) {
		_datadisks->__getitem__(k)->flush();
	}
	Block *hdr = ConstBlock(0);
	_logdisk->write(LOG_BID_HEADER_BLOCK, hdr);
	_logdisk->flush();
}

void WALDisk::__recover() {
	Block *hdr_bid1 = _logdisk->read(LOG_BID_HEADER_BLOCK);
	Block *hdr_dev1 = _logdisk->read(LOG_DEV_HEADER_BLOCK);
	Block *hdr_bid2 = _logdisk->read(LOG_BID_HEADER_BLOCK + 1);
	Block *hdr_dev2 = _logdisk->read(LOG_DEV_HEADER_BLOCK + 1);
	uint64_t n = hdr_bid1->__getitem__(0);
	for (uint64_t i = 0; i < LOG_MAX_ENTRIES; ++ i) {
		uint64_t dev = 0;
		uint64_t bid = 0;
		if (i < PER_BLOCK) {
			dev = hdr_dev1->__getitem__(1 + i);
			bid = hdr_bid1->__getitem__(1 + i);
		} else {
			dev = hdr_dev2->__getitem__(i - PER_BLOCK);
			bid = hdr_bid1->__getitem__(i - PER_BLOCK);
		}
		Block *data = _logdisk->read(LOG_HEADER_BLOCK + i + 1);
		for (uint64_t k = 0; k < _datadisks->__len__(); ++ k) {
			_datadisks->__getitem__(k)->write(bid, data, And(dev == k, ULT(i, n)));
		}
	}
	__commit();
}

Block* WALDisk::_read(uint64_t dev, uint64_t bid) {
	return read(dev, bid);
}

Block* WALDisk::read(uint64_t dev, uint64_t bid) {
	Block *rdata = _datadisks->__getitem__(dev)->read(bid);
	return _cache->get3(dev, bid, rdata);
}


