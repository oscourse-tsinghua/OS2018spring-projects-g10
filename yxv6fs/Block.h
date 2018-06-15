#include "fs.h"

class Block {
    private:
        uint8_t* buf;
        uint64_t size;
    public:
        Block(uint64_t _size) {
            buf = (uint8_t*) calloc(size, sizeof(char));
            size = _size / sizeof(uint8_t);
        }
};