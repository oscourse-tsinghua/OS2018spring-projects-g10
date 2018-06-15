#include "fs.h"

class Block {
    private:
    public:
        uint8_t buf[BSIZE];
        uint64_t size;
        Block(uint64_t _size) {
            size = _size / sizeof(uint8_t);
        }
        uint64_t __getitem__(uint64_t key) {
            return buf[key];
        }
};