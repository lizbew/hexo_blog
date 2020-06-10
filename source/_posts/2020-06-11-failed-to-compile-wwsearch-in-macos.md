---
title: macOS下编译wwsearch 趟坑
date: 2020-06-11 00:15:59
tags: [wwsearch, cmake, macos]
---

wwsearch 是腾讯开源的搜索引擎， 尝试着在macos下编译，但遇到在大坑，过不了，只好放弃了。有时间去macos下的折腾编译的时间，还不如去翻下源码了解原理， 真要使用的话就去找台linux主机来编译。得有目的去折腾。 这里记录下其中的第一步。

项目代码 https://github.com/Tencent/wwsearch

根据git代码仓库指示，build过程是很简单的， 新建build子目录后，在build子目录下先`cmake ..` 再`make -j32`。

我在macos使用HomeBrew安装了cmake, 然后运行cmake时遇到如下错误：

```
-- Could NOT find GFLAGS (missing: GFLAGS_INCLUDE_DIR GFLAGS_LIBRARY)
-- Enabling RTTI in Debug builds only (default)
CMake Error at /usr/local/Cellar/cmake/3.15.5/share/cmake/Modules/FindPackageHandleStandardArgs.cmake:137 (message):
  Could NOT find Threads (missing: Threads_FOUND)
Call Stack (most recent call first):
  /usr/local/Cellar/cmake/3.15.5/share/cmake/Modules/FindPackageHandleStandardArgs.cmake:378 (_FPHSA_FAILURE_MESSAGE)
  /usr/local/Cellar/cmake/3.15.5/share/cmake/Modules/FindThreads.cmake:220 (FIND_PACKAGE_HANDLE_STANDARD_ARGS)
  deps/rocksdb/CMakeLists.txt:447 (find_package)
```

关键信息就是 `Could NOT find GFLAGS (missing: GFLAGS_INCLUDE_DIR GFLAGS_LIBRARY)` 与`missing: Threads_FOUND`

构建wwsearch实际是依赖GFlags的，项目文档并未说明。 在cmake/modules/FindGFlags.cmake中定义了查找gflags的过程。 解决办是Homebrew安装gflags.

```bash
brew install gflags
```

而`missing: Threads_FOUND`则是rocksdb报的错误。网上搜索一番，不建议直接编译rocksdb, 而是使用brew来安装，或者是使用gcc来编译。 于是在这里放弃了

本文也发布于知乎上 https://zhuanlan.zhihu.com/p/147085153
