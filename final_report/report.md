# 操作系统 大实验 g10 Verification of File Systems 最终报告

							2015011358，陈经基
							2015011347，朱昊


<!-- vim-markdown-toc GFM -->

* [背景介绍](#背景介绍)
* [任务介绍](#任务介绍)
* [掉电安全文件系统介绍](#掉电安全文件系统介绍)
	* [Crash-Refinement的形式化定义](#crash-refinement的形式化定义)
		* [Definition 1](#definition-1)
		* [Definition 2](#definition-2)
		* [Definition 3](#definition-3)
		* [Definition 4](#definition-4)
		* [Definition 5](#definition-5)
	* [掉电文件系统开发流程](#掉电文件系统开发流程)
* [Yggdrasil代码介绍与分析](#yggdrasil代码介绍与分析)
	* [环境设置](#环境设置)
	* [Yhv6文件系统结构](#yhv6文件系统结构)
	* [Yggdrasil代码](#yggdrasil代码)
		* [符号执行引擎](#符号执行引擎)
		* [Z3 SMT Solver](#z3-smt-solver)
* [hv6 OS分析与介绍](#hv6-os分析与介绍)
	* [LLVMPy Emmiter](#llvmpy-emmiter)
	* [hv6文件系统](#hv6文件系统)
* [工作计划](#工作计划)
* [任务分工](#任务分工)
* [实验收获](#实验收获)
* [参考文献](#参考文献)

<!-- vim-markdown-toc -->

## 背景介绍

## 任务介绍

## 掉电安全文件系统介绍

### Crash-Refinement的形式化定义

#### Definition 1
#### Definition 2
#### Definition 3
#### Definition 4
#### Definition 5

### 掉电文件系统开发流程

## Yggdrasil代码介绍与分析

### 环境设置

### Yhv6文件系统结构

### Yggdrasil代码

#### 符号执行引擎

#### Z3 SMT Solver

## hv6 OS分析与介绍

### LLVMPy Emmiter
#### PyEmitter
##### Emitter.hh & Emitter.cc

* The Emitter class is in `namespace irpy`
* Member: an ostream and an indent level
* Only constructed by calling Emitter(stream = stream, indent_level = 0)
* Two methods: 
    1. line(string) indents for indent_level times and output the string
    2. line(void) output a return symbol

##### PyEmitter.hh & PyEmitter.cc

* PyEmitter is a subclass of Emitter
* Constructed by calling PyEmitter(stream)
* Four methods:
    1. genBlock(string, function<void()>) output the block + ":"; indent; execute the function; unindent
    2. genDef(string, vector<string>, function<void()>) output "def " + function's name + "(" + args' names + ")" + ":"; indent; excute function; unindent
    3. genException(string) output an Exception message
    4. emitWarning(string) give warning that this file is automatically generate from another file.

##### PyLLVMEmitter.hh && PyLLVMEmitter.cc

* PyLLVMEmitter is a subclass of PyEmitter
* Constructed by calling PyLLVMEmitter(stream, module) module is an instance of LLVM:Module
* Six methods:
    1. emitModule(void) 
    2. emitMetadata(void);
    3. emitBasicBlock(llvm::BasicBlock &bb);
    4. emitStructType(const llvm::StructType &type);
    5. emitFunction(llvm::Function &func);
    6. emitGlobalVariable(const llvm::GlobalVariable &type);
* function quoto(string) add quotes to a string
* function nameType(llvm::Value) return "itypes.parse_type(ctx," + the Value's type + ")"
* function getPrintingName(llvm::Value, bool, llvm::Module) return the name of this llvm::Value
* MetadataVisitor is a subclass of llvm::InstVisitor<MetadataVisitor>
* Constructed by MetadataVisitor(llvm::Module, bool) the Module to visit and recursive or not
* Four methods:
    1. addMDNode(llvm::MDNode) add this MDNode to the set of meta data nodes; if recursive also add its operands
    2. visitFunction(llvm::Function) add all metadata attached to the function
    3. visitInstruction(llvm::Instruction) add all metadata attached to the instruction
    4. getMetaData(void) get the list of identifier, metadata pairs
* PyInstVisitor is a subclass of llvm::InstVisitor<PyInstVisitor>
* Constructed by PyInstVisitor(PyEmitter, llvm::Module) 
* 32 functions:
    1. genPyCallFromInstruction(bool, string, T, kwargs_t)
    2. genPyCall(string, args_t, kwargs_t) together with _genPyCall(stringm, args_t, kwargs_t) generate a function call "irpy."+string(ctx, args, kwargs)
    3. name(llvm::Value) get the name of Value
    4. get(llvm::Value) if Value is an instruction, it returns ctx.stack["name(i)"]; if Value is a constant, it returns visitConstant(Value); if Value is am Argument, it returns ctx.stack["name(i)"]; if Value is an InlineAsm, it returns python function call asm + asmstring with quote.

### hv6文件系统

## 工作计划

## 任务分工

## 实验收获

## 参考文献
