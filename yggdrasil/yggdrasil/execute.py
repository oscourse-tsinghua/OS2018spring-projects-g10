import os
import subprocess
import unittest
import random

import z3
import libirpy
import libirpy.util

import sys


def execute(name, real_params, *args):
    module = __import__(name) # import name, a py file
    params = []

    for i in args:
        if isinstance(i, tuple):
            i = i[0]
        params.append(libirpy.util.FreshBitVec('param', i))

    def nop(*args, **kwargs):
        pass

    ctx = libirpy.newctx()
    libirpy.initctx(ctx, module)

    ctx['globals']['@llvm_lifetime_start'] = nop
    ctx['globals']['@llvm_lifetime_end'] = nop
    ctx['globals']['@llvm_lifetime_start_p0i8'] = nop
    ctx['globals']['@llvm_lifetime_end_p0i8'] = nop

    expr = ctx.call("@test", *params)
     
    subst = []
    for v, sym in zip(real_params, params):
        subst.append((sym, v)) # real params and symbolic params

    res = z3.simplify(z3.substitute(expr, subst)) # substitution, z3.simplify remove symbolic symbols; 
                                                 # since all symbols are substituted; it simplifies to output
    
    return res
