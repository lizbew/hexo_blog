---
title: Access HBase via thrift API
date: 2016-08-28 11:03:04
tags:
- HBase
- Hadoop
- thrift
- python
---

## 下载thrift

开发环境是在windows下，[apache thrift](http://thrift.apache.org/) 提供了windows的预编译文件，直接下载即可。
使用如下命令由__\*.thrift__文件生成python代码， 在子文件夹`gen-py`下， 在python代码中需要将该文件夹路径添加至`sys.path`。

{% codeblock lang:bash %}
thrift --gen py <Thrift filename>
{% endcodeblock %}

第一次使用thrift, 出现了个小乌龙，错将参数写成*--gen python*， 然后命令行出错，说无法找到generator python。 为这个错误还在网上搜索了老半天。

## HBase thrift 接口

在[HBase文档](http://hbase.apache.org/book.html#_thrift)中没有明确给出thift接口的使用方法， 使用搜索引擎才找到用法。

HBase thrift 接口有两个版本，称为`thrift`和`thrift2`， 可以从HBase的源码包拿到，压缩包中相应的路径分别是 **hbase-thrift/src/main/resources/org/apache/hadoop/hbase/thrift/Hbase.thrift** 和 **hbase-thrift/src/main/resources/org/apache/hadoop/hbase/thrift2/hbase.thrift**. 这里使用的是`thrift2`接口。

另外HBase thrift service 需要单独启动。 thrift和thrift2 使用相同的端口`9090`，默认配置下只能使用其中一种。

* start/stop thrift:
{% codeblock lang:bash %}
$HBASE_HOME/bin/hbase-daemon.sh start thrift
$HBASE_HOME/bin/hbase-daemon.sh stop thrift
{% endcodeblock %}

* start/stop thrift2:
{% codeblock lang:bash %}
$HBASE_HOME/bin/hbase-daemon.sh start thrift2
$HBASE_HOME/bin/hbase-daemon.sh stop thrift2
{% endcodeblock %}

* 检查端口占用
{% codeblock lang:bash %}
netstat -nao | grep 9090
{% endcodeblock %}

参考：
* [HBase wiki](http://wiki.apache.org/hadoop/Hbase/ThriftApi)
* [ Thrift介绍与应用（三）—hbase的thrift接口](http://blog.csdn.net/guxch/article/details/12163047)
* [Guide to Using Apache HBase Ports](https://blog.cloudera.com/blog/2013/07/guide-to-using-apache-hbase-ports/)

## python代码，查询HBase数据

生成的python代码中client访问HBase使用类`hbase.THBaseService.Client`, 只支持数据操作，不能对表结构作查询或是变更。

{% codeblock lang:python %}
  #!/usr/bin/env python

  import sys

  sys.path.append('gen-py')

  from thrift import Thrift
  from thrift.transport import TSocket
  from thrift.transport import TTransport
  from thrift.protocol import TBinaryProtocol

  from hbase import THBaseService
  from hbase.ttypes import *

  try:
      transport = TSocket.TSocket('localhost', 9090)
      transport = TTransport.TBufferedTransport(transport)
      protocol = TBinaryProtocol.TBinaryProtocol(transport)

      client = THBaseService.Client(protocol)
      transport.open()

      scannerId = None
      try:
          scannerId = client.openScanner('test', TScan())
          rows = client.getScannerRows(scannerId, 1)
          if rows:
              for r in rows:
                  print r.row
                  for c in r.columnValues:
                      print '\t{}:{} - {}'.format(c.family, c.qualifier, c.value)
      except Exception, e:
          print e
      finally:
          if scannerId:
              client.closeScanner(scannerId)

  except Thrift.TException, tx:
      print '%s' % (tx.message)
{% endcodeblock %}

## Thrift 函数默认参数的问题

在`hbase.thrit`中`getScannerRows(scannerId, numRows)`第二个参数`numRows`有指明默认值为*1*，
但生成的python代码并没有默认参数。

hbase.thrift:
![hbase.thrift](/images/post/2016-08-28-thrift1.png)

THBaseService.py:
![THBaseService.py](/images/post/2016-08-28-thrift2.png)
