from z3 import *
import disk
from waldisk import *
import unittest
import itertools
from waldisk import TripleList, PartitionAsyncDiskList

from yggdrasil.ufarray import *
from yggdrasil.util import *
from yggdrasil.diskspec import *
from yggdrasil import test


# to verify that WALDisk is a crash-refinement of MultiTxnDisk
# so, corresponding to layer2 transaction disk
# ... I see... WALDisk is ... write-ahead logging disk (so transaction disk)

class WALDiskTestRefinement(test.RefinementTest):
    def create_spec(self, mach):
        dataarray1 = FreshDiskArray('dataarray')
        dataarray2 = FreshDiskArray('dataarray')
        return MultiTxnDisk(mach, [dataarray1, dataarray2])

    def create_impl(self, mach, logarray=None):
        # reuse the logarray (or a physical disk)
        # i guess that FreshDiskArray is the specification of a physical block decice
        if logarray is None:
            logarray = ConstDiskArray(ConstBlock(0))
        dataarray1 = FreshDiskArray('dataarray')
        dataarray2 = FreshDiskArray('dataarray')
        # a logdisk along with two data disk? so a transaction disk 
        logdisk = AsyncDisk(mach, logarray)
        datadisk1 = AsyncDisk(mach, dataarray1)
        datadisk2 = AsyncDisk(mach, dataarray2)
        return WALDisk(logdisk, PartitionAsyncDiskList([datadisk1, datadisk2]), osync=False)

    def equivalence_volatile(self, spec, impl, **kwargs):
        # (spec <=> impl) <=> (same content)
        # I think that FreshSize of a wrapper of some Z3 class like BitVector
        # disk-buffer 
        bid = FreshSize('bid')
        return ForAll([bid], And(
            spec.read(0, bid) == impl.read(0, bid), # SMT encoding as output
            spec.read(1, bid) == impl.read(1, bid)))

    def equivalence_durable(self, spec, impl, **kwargs):
        bid = FreshSize('bid')
        return ForAll([bid], And(
            spec._disks[0](bid) == impl._datadisks[0].read(bid),
            spec._disks[1](bid) == impl._datadisks[1].read(bid)))

    equivalence = equivalence_volatile

    def call_write_tx_nocommit(self, spec, impl, args):
        impl.begin_tx()
        spec.begin_tx()

        #print "*************"
        #print type(args)
        for arg in args[0]:
            impl.write_tx(*arg)
            spec.write_tx(*arg)

    def call_write_tx(self, spec, impl, args):
        impl.begin_tx()
        spec.begin_tx()

        for arg in args[0]:
            impl.write_tx(*arg)
            spec.write_tx(*arg)

        impl.commit_tx()
        spec.commit_tx()

    def _gen_iov(self, *args, **kwargs):
        # ?????
        for n in range(WALDisk.LOG_MAX_ENTRIES + 1):
            iov = []
            for i in range(n):
                iov.append((1, FreshSize('i'), FreshBlock('x')))
            iov_list = TripleList(iov)
            #yield (iov,)
            yield (iov_list,)

    # Verify writev
    match_writev = _gen_iov
    match_write_tx = _gen_iov
    match_write_tx_nocommit = lambda self, *args, **kwargs: self._gen_iov(*args, **kwargs)
    match_write_tx_nocommit.nocrash = True

    # recover-full(recover-partial(d)) = recover-full(d)
    # entry function
    def test_idempotent_recovery(self):
        mach = Machine()
        logarray = FreshDiskArray('logarray')
        d = self.create_impl(mach, logarray=logarray)
        assumption = mach.assumption

        # Recovery post-condition..
        # to make sure that after the recovery, first entry if logdisk(count) is 0
        self.solve(assumption, mach._on,
                d._logdisk._disk(0)[0] != 0)

        # block i after a full recovery
        i = FreshSize('i')
        x = d.read(0, i)

        # block i after a partial recovery followed by a full recovery
        mach = Machine()
        y = d.crash(mach).read(0, i)
        assumption = And(assumption, mach.assumption)

        # make sure that recovery operation is idempotent
        self.solve(assumption, Not(x == y))

    # another entry function
    def test_atomic(self):
        for i in range(2):
            self.__test_atomic(i + 1)

    def __test_atomic(self, n):
        mach = Machine()
        d = self.create_impl(mach)

        bids = [FreshSize('i') for i in range(n)]
        xs = [FreshBlock('x') for i in range(n)]
        iov = zip(itertools.repeat(0), bids, xs)

        oldvs = [d.read(0, bid) for bid in bids]

        iov_list = TripleList(iov)
        """
        iov_list._is_none = False
        iov_list.__len__ = len(iov)
        iov_list._txn = iov
        """

        d.writev(iov_list)
        """
        d.writev(iov)
        """

        assumption = And(Distinct(*bids), mach.assumption)

        # reboot & recovery
        mach = Machine()
        d = d.crash(mach)
        anyvs = [d.read(0, bid) for bid in bids]

        # prove the atomic of every transaction
        self.prove(Implies(assumption, Or(
            And(*[anyv == oldv for anyv, oldv in zip(anyvs, oldvs)]),
            And(*[anyv == x for anyv, x in zip(anyvs, xs)]))))
        
        # note that self.prove(X) is to prove that X is valid
        # and self.solve(X) is to prove that X is never satisfied


if __name__ == '__main__':
    test.main()
