#ifndef ASYNCDISK_H
#define AYSNCDISK_H

#include "user.h"

class AsyncDisk {
	public:
		AsyncDisk();
		void write(uint bid, uint8_t *data);
		void read(uint bid, uint8_t *data);
		void flush();
};

#endif
