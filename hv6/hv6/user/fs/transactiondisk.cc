#include "transactiondisk.h"
#include "user.h"

TransactionDisk::TransactionDisk(AsyncDisk *logdisk, void* datadisks, bool osync=true) {
	this->LOG_BID_HEADER_BLOCK = 0;
	this->LOG_DEV_HEADER_BLOCK = 2;
	this->LOG_HEADER_BLOCK = 3;

	this->PER_BLOCK = 511;

	this->_osync = osync;
	this->_logdisk = logdisk;
	this->_datadisks = datadisks;

	this->__recover();
	this->num_txn = 0;
	this->_cache = Dict();
}

void TransactionDisk::begin_tx() {
	if ((not this->_osync) and (this->num_txn > 0)) {
		return ;
	}
	assert(this->num_txn == 0, "begin_tx num_txn is not 0");
	this->num_txn = 0;
	this->_cache = Dict();
}

void TransactionDisk::write_tx(uint dev, uint bid, uint8_t *data) {
}

void TransactionDisk::write(uint dev, uint bid, uint8_t *data) {
	this->_datadisks[dev]->write(bid, data);
}

void TransactionDisk::flush
