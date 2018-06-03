#
# WARNING: This file has been automatically generated from irpy/o.test/add_0.ll
#

import libirpy.itypes as itypes

def _init_types(ctx,):
  irpy = ctx['eval']


def _init_globals(ctx,):
  irpy = ctx['eval']
  irpy.declare_global_constant(ctx,'@_str',itypes.parse_type(ctx,'[4 x i8]*'),irpy.constant_data_array(ctx,itypes.parse_type(ctx,'[4 x i8]'),'c"%u\0A\00"',),itypes.parse_type(ctx,'[4 x i8]'))


def func_test(ctx,arg1,arg2,):
  irpy = ctx['eval']
  ctx['stacktrace'][-1] = {'function':'test'}
  assert itypes.has_type(ctx, arg1, itypes.parse_type(ctx,'i32')), 'Incorrect BitVec size'
  ctx.stack["%0"] = arg1
  assert itypes.has_type(ctx, arg2, itypes.parse_type(ctx,'i32')), 'Incorrect BitVec size'
  ctx.stack["%1"] = arg2
  def bb_2(pred,):
    ctx.stack["%3"] = irpy.alloca(ctx,itypes.parse_type(ctx,'i32*'),irpy.constant_int(ctx,1,32,),itypes.parse_type(ctx,'i32'),)
    ctx.stack["%4"] = irpy.alloca(ctx,itypes.parse_type(ctx,'i32*'),irpy.constant_int(ctx,1,32,),itypes.parse_type(ctx,'i32'),)
    irpy.store(ctx,itypes.parse_type(ctx,'void'),ctx.stack["%0"],itypes.parse_type(ctx,'i32'),ctx.stack["%3"],itypes.parse_type(ctx,'i32*'),)
    irpy.store(ctx,itypes.parse_type(ctx,'void'),ctx.stack["%1"],itypes.parse_type(ctx,'i32'),ctx.stack["%4"],itypes.parse_type(ctx,'i32*'),)
    irpy.debug_loc(ctx,'%5','irpy/test/add.c:23:12',)
    ctx.stack["%5"] = irpy.load(ctx,itypes.parse_type(ctx,'i32'),ctx.stack["%3"],itypes.parse_type(ctx,'i32*'),)
    irpy.debug_loc(ctx,'%6','irpy/test/add.c:23:16',)
    ctx.stack["%6"] = irpy.load(ctx,itypes.parse_type(ctx,'i32'),ctx.stack["%4"],itypes.parse_type(ctx,'i32*'),)
    irpy.debug_loc(ctx,'%7','irpy/test/add.c:23:14',)
    ctx.stack["%7"] = irpy.add(ctx,itypes.parse_type(ctx,'i32'),ctx.stack["%5"],itypes.parse_type(ctx,'i32'),ctx.stack["%6"],itypes.parse_type(ctx,'i32'),)
    irpy.debug_loc(ctx,'<badref>','irpy/test/add.c:23:5',)
    return ctx.stack["%7"]

  return bb_2(None)

def func_main(ctx,arg1,arg2,):
  irpy = ctx['eval']
  ctx['stacktrace'][-1] = {'function':'main'}
  assert itypes.has_type(ctx, arg1, itypes.parse_type(ctx,'i32')), 'Incorrect BitVec size'
  ctx.stack["%0"] = arg1
  assert itypes.has_type(ctx, arg2, itypes.parse_type(ctx,'i8**')), 'Incorrect BitVec size'
  ctx.stack["%1"] = arg2
  def bb_2(pred,):
    ctx.stack["%3"] = irpy.alloca(ctx,itypes.parse_type(ctx,'i32*'),irpy.constant_int(ctx,1,32,),itypes.parse_type(ctx,'i32'),)
    ctx.stack["%4"] = irpy.alloca(ctx,itypes.parse_type(ctx,'i32*'),irpy.constant_int(ctx,1,32,),itypes.parse_type(ctx,'i32'),)
    ctx.stack["%5"] = irpy.alloca(ctx,itypes.parse_type(ctx,'i8***'),irpy.constant_int(ctx,1,32,),itypes.parse_type(ctx,'i32'),)
    ctx.stack["%6"] = irpy.alloca(ctx,itypes.parse_type(ctx,'i32*'),irpy.constant_int(ctx,1,32,),itypes.parse_type(ctx,'i32'),)
    irpy.store(ctx,itypes.parse_type(ctx,'void'),irpy.constant_int(ctx,0,32,),itypes.parse_type(ctx,'i32'),ctx.stack["%3"],itypes.parse_type(ctx,'i32*'),)
    irpy.store(ctx,itypes.parse_type(ctx,'void'),ctx.stack["%0"],itypes.parse_type(ctx,'i32'),ctx.stack["%4"],itypes.parse_type(ctx,'i32*'),)
    irpy.store(ctx,itypes.parse_type(ctx,'void'),ctx.stack["%1"],itypes.parse_type(ctx,'i8**'),ctx.stack["%5"],itypes.parse_type(ctx,'i8***'),)
    irpy.debug_loc(ctx,'%7','irpy/test/add.c:28:30',)
    ctx.stack["%7"] = irpy.load(ctx,itypes.parse_type(ctx,'i8**'),ctx.stack["%5"],itypes.parse_type(ctx,'i8***'),)
    irpy.debug_loc(ctx,'%8','irpy/test/add.c:28:30',)
    ctx.stack["%8"] = irpy.get_element_ptr(ctx,itypes.parse_type(ctx,'i8**'),ctx.stack["%7"],itypes.parse_type(ctx,'i8**'),irpy.constant_int(ctx,1,64,),itypes.parse_type(ctx,'i64'),inbounds=True,nuw=True,)
    irpy.debug_loc(ctx,'%9','irpy/test/add.c:28:30',)
    ctx.stack["%9"] = irpy.load(ctx,itypes.parse_type(ctx,'i8*'),ctx.stack["%8"],itypes.parse_type(ctx,'i8**'),)
    irpy.debug_loc(ctx,'%10','irpy/test/add.c:28:25',)
    ctx.stack["%10"] = irpy.call(ctx,itypes.parse_type(ctx,'i32'),ctx.stack["%9"],itypes.parse_type(ctx,'i8*'),irpy.global_value(ctx,itypes.parse_type(ctx,'i32 (i8*)*'),'@atoi',),itypes.parse_type(ctx,'i32 (i8*)*'),)
    irpy.debug_loc(ctx,'%11','irpy/test/add.c:28:45',)
    ctx.stack["%11"] = irpy.load(ctx,itypes.parse_type(ctx,'i8**'),ctx.stack["%5"],itypes.parse_type(ctx,'i8***'),)
    irpy.debug_loc(ctx,'%12','irpy/test/add.c:28:45',)
    ctx.stack["%12"] = irpy.get_element_ptr(ctx,itypes.parse_type(ctx,'i8**'),ctx.stack["%11"],itypes.parse_type(ctx,'i8**'),irpy.constant_int(ctx,2,64,),itypes.parse_type(ctx,'i64'),inbounds=True,nuw=True,)
    irpy.debug_loc(ctx,'%13','irpy/test/add.c:28:45',)
    ctx.stack["%13"] = irpy.load(ctx,itypes.parse_type(ctx,'i8*'),ctx.stack["%12"],itypes.parse_type(ctx,'i8**'),)
    irpy.debug_loc(ctx,'%14','irpy/test/add.c:28:40',)
    ctx.stack["%14"] = irpy.call(ctx,itypes.parse_type(ctx,'i32'),ctx.stack["%13"],itypes.parse_type(ctx,'i8*'),irpy.global_value(ctx,itypes.parse_type(ctx,'i32 (i8*)*'),'@atoi',),itypes.parse_type(ctx,'i32 (i8*)*'),)
    irpy.debug_loc(ctx,'%15','irpy/test/add.c:28:20',)
    ctx.stack["%15"] = irpy.call(ctx,itypes.parse_type(ctx,'i32'),ctx.stack["%10"],itypes.parse_type(ctx,'i32'),ctx.stack["%14"],itypes.parse_type(ctx,'i32'),irpy.global_value(ctx,itypes.parse_type(ctx,'i32 (i32, i32)*'),'@test',),itypes.parse_type(ctx,'i32 (i32, i32)*'),)
    irpy.debug_loc(ctx,'<badref>','irpy/test/add.c:28:14',)
    irpy.store(ctx,itypes.parse_type(ctx,'void'),ctx.stack["%15"],itypes.parse_type(ctx,'i32'),ctx.stack["%6"],itypes.parse_type(ctx,'i32*'),)
    irpy.debug_loc(ctx,'%16','irpy/test/add.c:29:20',)
    ctx.stack["%16"] = irpy.load(ctx,itypes.parse_type(ctx,'i32'),ctx.stack["%6"],itypes.parse_type(ctx,'i32*'),)
    irpy.debug_loc(ctx,'%17','irpy/test/add.c:29:5',)
    ctx.stack["%17"] = irpy.call(ctx,itypes.parse_type(ctx,'i32'),irpy.getelementptr(ctx,itypes.parse_type(ctx,'i8*'),irpy.global_value(ctx,itypes.parse_type(ctx,'[4 x i8]*'),'@_str',),itypes.parse_type(ctx,'[4 x i8]*'),irpy.constant_int(ctx,0,32,),itypes.parse_type(ctx,'i32'),irpy.constant_int(ctx,0,32,),itypes.parse_type(ctx,'i32'),),itypes.parse_type(ctx,'i8*'),ctx.stack["%16"],itypes.parse_type(ctx,'i32'),irpy.global_value(ctx,itypes.parse_type(ctx,'i32 (i8*, ...)*'),'@printf',),itypes.parse_type(ctx,'i32 (i8*, ...)*'),)
    irpy.debug_loc(ctx,'<badref>','irpy/test/add.c:30:5',)
    return irpy.constant_int(ctx,0,32,)

  return bb_2(None)

def _init_metadata(ctx,):
  irpy = ctx['eval']
  irpy.declare_metadata(ctx, '!0','distinct !DICompileUnit(language: DW_LANG_C99, file: !1, producer: "clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !2)')
  irpy.declare_metadata(ctx, '!1','!DIFile(filename: "irpy/test/add.c", directory: "/root/OS2018spring-projects-g10/hv6")')
  irpy.declare_metadata(ctx, '!2','!{}')
  irpy.declare_metadata(ctx, '!7','distinct !DISubprogram(name: "test", scope: !1, file: !1, line: 21, type: !8, isLocal: false, isDefinition: true, scopeLine: 22, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)')
  irpy.declare_metadata(ctx, '!8','!DISubroutineType(types: !9)')
  irpy.declare_metadata(ctx, '!9','!{!10, !10, !10}')
  irpy.declare_metadata(ctx, '!10','!DIDerivedType(tag: DW_TAG_typedef, name: "uint32_t", file: !11, line: 51, baseType: !12)')
  irpy.declare_metadata(ctx, '!11','!DIFile(filename: "/usr/include/stdint.h", directory: "/root/OS2018spring-projects-g10/hv6")')
  irpy.declare_metadata(ctx, '!12','!DIBasicType(name: "unsigned int", size: 32, encoding: DW_ATE_unsigned)')
  irpy.declare_metadata(ctx, '!15','!DILocation(line: 21, column: 24, scope: !7)')
  irpy.declare_metadata(ctx, '!17','!DILocation(line: 21, column: 36, scope: !7)')
  irpy.declare_metadata(ctx, '!18','!DILocation(line: 23, column: 12, scope: !7)')
  irpy.declare_metadata(ctx, '!19','!DILocation(line: 23, column: 16, scope: !7)')
  irpy.declare_metadata(ctx, '!20','!DILocation(line: 23, column: 14, scope: !7)')
  irpy.declare_metadata(ctx, '!21','!DILocation(line: 23, column: 5, scope: !7)')
  irpy.declare_metadata(ctx, '!22','distinct !DISubprogram(name: "main", scope: !1, file: !1, line: 26, type: !23, isLocal: false, isDefinition: true, scopeLine: 27, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)')
  irpy.declare_metadata(ctx, '!23','!DISubroutineType(types: !24)')
  irpy.declare_metadata(ctx, '!24','!{!25, !25, !26}')
  irpy.declare_metadata(ctx, '!25','!DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)')
  irpy.declare_metadata(ctx, '!26','!DIDerivedType(tag: DW_TAG_pointer_type, baseType: !27, size: 64)')
  irpy.declare_metadata(ctx, '!27','!DIDerivedType(tag: DW_TAG_pointer_type, baseType: !28, size: 64)')
  irpy.declare_metadata(ctx, '!28','!DIBasicType(name: "char", size: 8, encoding: DW_ATE_signed_char)')
  irpy.declare_metadata(ctx, '!30','!DILocation(line: 26, column: 14, scope: !22)')
  irpy.declare_metadata(ctx, '!32','!DILocation(line: 26, column: 27, scope: !22)')
  irpy.declare_metadata(ctx, '!34','!DILocation(line: 28, column: 14, scope: !22)')
  irpy.declare_metadata(ctx, '!35','!DILocation(line: 28, column: 30, scope: !22)')
  irpy.declare_metadata(ctx, '!36','!DILocation(line: 28, column: 25, scope: !22)')
  irpy.declare_metadata(ctx, '!37','!DILocation(line: 28, column: 45, scope: !22)')
  irpy.declare_metadata(ctx, '!38','!DILocation(line: 28, column: 40, scope: !22)')
  irpy.declare_metadata(ctx, '!39','!DILocation(line: 28, column: 20, scope: !22)')
  irpy.declare_metadata(ctx, '!40','!DILocation(line: 29, column: 20, scope: !22)')
  irpy.declare_metadata(ctx, '!41','!DILocation(line: 29, column: 5, scope: !22)')
  irpy.declare_metadata(ctx, '!42','!DILocation(line: 30, column: 5, scope: !22)')

