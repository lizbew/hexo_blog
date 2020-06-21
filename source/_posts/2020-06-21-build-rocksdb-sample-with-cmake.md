---
title: 构建一个rocksdb示例程序
date: 2020-06-21 11:22:55
tags: [cmake, rocksdb]
---

编译wwsearch 趟坑后，使用brew install rocksdb 安装了rocksdb库， 然后对照着网上代码写了一个使用rocksdb的PUT/GET操作简单程序， cmake构建。

直接上代码， 主文件为 test_rocksdb.cxx。创建rocksdb的库的路径为./testdb, db打开之后先Put一个key为key-one的值， 然后再Get操作获取相同的key, 打印出来。

```cpp
#include <iostream>

#include "rocksdb/db.h"
int main(int argc, char *argv[]) 
{
    rocksdb::DB* db;
    rocksdb::Options options;
    options.create_if_missing = true;
    rocksdb::Status status = rocksdb::DB::Open(options, "./testdb", &db);
    std::cout << "rocksb open status: " << status.ok() << std::endl;

    std::string sKey("key-one");
    std::string sValue("Value Some");
    
    status = db->Put(rocksdb::WriteOptions(), sKey, sValue);
    if (status.ok()) 
    {
        std::cout << "put key ok" << std::endl;
        std::string rValue;
        rocksdb::Status s = db->Get(rocksdb::ReadOptions(), sKey, &rValue);
        if (s.ok()) {
            std::cout << "read from rocksdb success: " << rValue << std::endl;
        }
    } 
    else 
    {
        std::cout << "put key error, with status: " << status.code() << std::endl;
    }

    db->Close();
    
    return 0;
}
```
如下是CMakeLists.txt文件的内容

```cmake
cmake_minimum_required(VERSION 2.8.12)

project(test_rocksdb)
# Enable C++11
set(CMAKE_CXX_STANDARD 11)

find_path(ROCKSDB_INCLUDE_DIR rocksdb/db.h
    PATHS "")
include_directories(${ROCKSDB_INCLUDE_DIR})

find_library(ROCKSDB_LIB rocksdb)
message(STATUS "finding ${ROCKSDB_LIB}")

add_executable(Test_rocksdb test_rocksdb.cxx)
target_link_libraries(Test_rocksdb ${ROCKSDB_LIB})
```

构建过程：

```bash
mkdir build && cd ./build
cmake .. && make
./Test_rocksdb
```

由于对cmake不熟悉，很久也没有c++方面编码，也是折腾了两天。

## 问题1： 运行make 时提示c++语言扩展的Warning，找不到kNone等一些语法错误

    /usr/local/include/rocksdb/cleanable.h:27:27: warning: deleted function definitions are a C++11 extension [-Wc++11-extensions]
    Cleanable(Cleanable&) = delete;
    ^ 

解决方法是在CMakeLists.txt中添加set(CMAKE_CXX_STANDARD11)， 支持c++11的语法

## 问题2： 找不到头文件

    ../c2-rocksdb/test_rocksdb.cxx:3:10: fatal error: 'rocksdb/db.h' file not found
    #include "rocksdb/db.h"
    ^~~~~~~~~~~~~~
    1 error generated.

解决方法:

```cmake
find_path(ROCKSDB_INCLUDE_DIR rocksdb/db.h
    PATHS "")
include_directories(${ROCKSDB_INCLUDE_DIR})
```

## 问题3： 链接失败

    [ 50%] Building CXX object CMakeFiles/Test_rocksdb.dir/test_rocksdb.cxx.o
    [100%] Linking CXX executable Test_rocksdb
    Undefined symbols for architecture x86_64:
    "rocksdb::ReadOptions::ReadOptions()", referenced from:
    _main in test_rocksdb.cxx.o

解决方法:

```cmake
find_library(ROCKSDB_LIB rocksdb)
message(STATUS "finding ${ROCKSDB_LIB}")
# ...

target_link_libraries(Test_rocksdb ${ROCKSDB_LIB})
```

## 运行程序

编译成功之后，./Test_rocksdb 运行程序，结束之后会在当前目录多出一个testdb目录。其中OPTIONS-000005文件中是ini格式的配置文件， LOG为rocksdb打印的日志。

    000003.log
    CURRENT
    IDENTITY
    LOCK
    LOG
    MANIFEST-000001
    OPTIONS-000005


