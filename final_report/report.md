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
文件系统是操作系统的一个不可缺少的组成成分。而硬盘上的数据结构非常复杂，进行验证与复现bug比较困难。在这个工作中，我们讨论如何写出并验证一个crash-safe的文件系统。

之前的文献中已经提及一个crash-safe的文件系统Yggdrasil，然而这个文件系统

## 任务介绍

接下来对本次大实验中所需要完成的实验任务进行简要介绍：

在本次实验中，我们最主要的工作在于对Yggdrasil这一用于验证掉电安全的文件系统的框架的代码与论文分别进行分析与理解，并且对代码进行注释，并且得到分析文档；其次对hv6操作系统的文件系统进行分析与理解，并且得到分析文档；在完成了足够的分析了解之后，将Yggdrasil中验证的使用cython实现的fuse文件系统Yxv6fs移植到使用C实现的hv6文件系统中，并且使用hv6中原先使用的符号执行框架，与Yggdrasil中进行掉电安全性验证的部分连接起来，从而使得hv6操作系统中拥有一个掉电安全的文件系统。

## 掉电安全文件系统介绍

在接下来将对掉电安全的文件系统进行介绍；在我们参考的论文中，使用了crash refinement作为了文件系统掉电安全性的形式化定义；在该形式化定义下，如果要验证某一个文件系统的掉电安全性，首先需要一份本身就应当被认为是安全的规范设置，称为specification，以及在每一个特定的磁盘状态下应当满足的不变量（表示为一阶谓词逻辑定理）；在拥有了specification的情况下，要求在当前文件系统实现在任何出现系统崩溃并且之后正确地执行了回复程序recovery之后的情况下，磁盘所处的状态与必须与某一个specification中执行了同一操作之后到达的状态等价（之所以说是某个状态，是因为认为specification中能够通过操作和系统奔溃的组合能够到达的所有状态都是合法的，因此特定一个specification中到达的状态，经过指定的某一次操作之后，能够到达的状态并不一定只有一个）；如果所有实现能够达到的磁盘状态均与specification能够达到的某状态想等价，则认为这个文件系统的实现是关于这个specification掉电安全的。

### Crash-Refinement的形式化定义

在下文中将对crash-refinement进行形式化定义：

#### Definition 1

在确定掉电安全性之前，首先需要的是所实现的文件系统能够符合规范的要求，因此需要要求在没有发生任何系统奔溃的情况下，文件系统的实现所能够到达的状态应该是specification中所允许的，因此，要求对于implement中的某一个状态s1与其对应的等价的specification中的状态s0，在执行完指定操作f之后，在发生掉电安全的情况下，他们所到达的状态仍然应当是等价的。

因此，形式化地描述在不发生系统奔溃情况下，实现能够符合规范要求的情况如下：

假设，f0是规范中描述的操作，而f1是实现中描述的操作，而他们所对应的系统不变量分别为I0, I1，则认为f1是在不掉电的情况下符合f0的要求（称之为f0与f1 crash-free equivalent）需要满足如下条件：
![def1](def1.png)


#### Definition 2

接下来描述在不具有recovery操作的情况下，在考虑了系统奔溃的可能下的情况下，需要怎样要求才能够认为实现满足规范的要求：由于所有允许的状态都是在规范中执行相应操作能够到达的状态，因此如果在实现中执行某一个操作，并且遭遇或者没有遭遇到系统奔溃的过程，最终到达的状态仍然能够与规范中允许的某一个状态想等价，则认为是实现本身还是符合了规范的要求；
因此，形式化地定义在考虑了系统奔溃的可能性，并且不考虑存在recovery操作的情况下，实现能够符合规范要求的情况如下：

假设，f0是规范中描述的操作，而f1是实现中描述的操作，而他们所对应的系统不变量分别为I0, I1，则认为f1在上述情况下符合f0的要求（称之为f1是f0的一个crash-refinement without recovery）需要满足如下条件：

![def2](def2.png)

#### Definition 3

由于在文件系统中，很有可能因为系统的奔溃，导致磁盘上维护的数据结构出现了不一致的情况，因此不少文件系统会在奔溃之后的其中的时候启动恢复操作，尝试恢复磁盘上文件系统的不一致性，这样的话文件系统的recovery操作使得文件系统的实现要符合规范的要求要更加简单一些，即不需要强硬的要求实现中执行完某一个操作，并且考虑了奔溃的情况下到达的状态一定需要与规范中要求的状态等价就可以了，而是只需要到达的状态在通过恢复操作之后可能到达与规范中的某个状态相等价的状态即可；自然，恢复操作的过程中也可能经历掉电的过程，在这种情况下，掉电这种情况显然不能够影响后续重启的时候执行的恢复操作的正确执行，因此，只要存在一次恢复操作成功了，就能够修复磁盘的不一致状态。

将上述性质称为了恢复操作的幂等性，将其进行形式化定义如下：

假设r是一个恢复函数，则其满足幂等性需要满足以下条件：

![def3](def3.png)

#### Definition 4

接下来讨论在存在恢复操作的情况下，实现能够符合规范的要求需要满足的形式化条件如下所示：

假设f0是规范中定义的某一个操作，而f1是实现中定义的与f0相对应的操作，而I0，I1分别是指这两个操作所需要满足的系统不变量，而r是幂等的恢复操作，而f0,f1本身在不考虑系统奔溃的情况下是等价的，则f1是满足了f0要求的实现（记为f1是f0的一个crash-refinement），则需要还满足的条件有：

![def4](def4.png)

#### Definition 5

由于存在某些操作不会对磁盘状态造成影响，因此对这些操作进行形式化定义如下：

![def5](def5.png)

#### Definition 6

接下来将文件系统F定义为文件系统的操作f的集合，则认为文件系统的实现F1满足了规范F0需要满足F1中所有的操作f1都满足了F0中对应的操作f0的要求；

### 掉电文件系统开发流程

接下来介绍开发掉电安全的文件系统的开发流程：

1. 编写文件系统需要满足的规范；
2. 编写需要满足的条件不变式；
3. 编写文件系统的实现；
4. 验证文件系统的实现满足规范；
5. 对文件系统的实现进行优化；

## Yggdrasil代码介绍与分析

### 环境设置

接下来简要介绍Yggdrasil和hv6的环境配置：

配置Yggdrasil环境：

1.  安装Z3
2.  安装fuse头文件，否则无法通过pkg-config正确获取相应的cflags
3.  创建文件系统的磁盘镜像
4.  创建fuse文件系统的挂载点（设置为a）
5.  编译yggdrasil
6.  挂载文件系统
7.  进行验证

配置hv6环境：

1. 安装qemu;
2. 更新编译工具;
3. 此时已经可以使用qemu运行hv6操作系统了;
4. 由于hv6原先实在ubuntu 17.10上编写的，使用的编译环境版本较高，使用make verify验证的时候有可能无法通过，因此需要对代码进行部分修改;
5. 使用make verify进行验证了;

最后环境配置成docker image，并且存放在docker hub上，分别为amadeuschan/osproject, amadeuschan/osproject_with_hv6，前者适用于yggdrasil中文件系统的验证与运行，而后者适用于两者的验证与运行；

此外，还在travis CI上配置了自动测试，由于travis CI默认需要10min内至少有一次对stdout的显式输出，而在yggdrasil中，某些test需要的时间要略长于10min，因此实现了后台脚本每隔10min往stdout输出的方式来欺骗travis CI平台，从而使得能够正确地完成测试。


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
