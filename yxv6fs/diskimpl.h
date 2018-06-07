#pragma once

class PartitionAsyncDisk {
};

class List {
	public:
		bool _is_none;
		List() {
			_is_none = true;
		}
		void setNone(bool is_none) {
			_is_none = is_none;
		}
		bool isNone() {
			return _is_none;
		}
		bool isNotNone() {
			return !_is_none;
		}
		void clear() {
			_is_none = false;
		}
};

class TripleList: public List{
};

class PartitionAsyncDiskList: public List{
};

class Dict {
};

class Block {
};
