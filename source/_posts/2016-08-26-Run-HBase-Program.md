---
title: Run HBase Program
date: 2016-08-26 16:17:55
tags:
- HBase
- Hadoop
- java
---

参考[HBase官方文档](http://hbase.apache.org/book.html#quickstart)，setup一个单机环境，使用HDFS。 这里主要记录下编译运行java代码访问HBase的相关的步骤， 都是从文档里参考而来。

## 依赖的jar包

访问HBase的代码也需要Hadoop相关的library, 所以我直接借用访问HDFS的工程，在里面添加了一个Class。
另外从hbase-bin-x.tar.gz里复制出两个library放到project/libs下：

* hbase-client-1.2.2.jar
* hbase-common-1.2.2.jar

## 关于代码

代码直接复制[Apache HBase APIs/Examples](http://hbase.apache.org/book.html#_examples).
在运行过程发现native lib问题，于是删除了`createSchemaTables()`中指定column-family的压缩格式：
`setCompressionType(Algorithm.SNAPPY)`。

下面未删除压缩格式之前遇到的Exception：

{% blockquote %}
Exception in thread "main" org.apache.hadoop.hbase.DoNotRetryIOException: org.apache.hadoop.hbase.DoNotRetryIOException: java.lang.RuntimeException: native snappy library not available: SnappyCompressor has not been loaded. Set hbase.table.sanity.checks to false at conf or table descriptor if you want to bypass sanity checks
{% endblockquote %}

## 运行

参考 [HBase and MapReduce](http://hbase.apache.org/book.html#mapreduce)

代码中引用到两个环境变量，在运行之前也要在bash环境上定义：`HBASE_CONF_DIR`和`HADOOP_CONF_DIR`。

{% codeblock lang:bash %}
HBASE_CONF_DIR=${HBASE_HOME}/conf HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop  HADOOP_CLASSPATH=`${HBASE_HOME}/bin/hbase classpath` ${HADOOP_HOME}/bin/hadoop jar /vagrant/tmp/HapTet-1.0-SNAPSHOT.jar com.viifly.hbase.ta1.HbaseT1
{% endcodeblock %}

可实际运行结果并不符合预期, `createSchemaTables()`正常， 但随后的`modifySchema()`却是表不存在！

{% blockquote %}
...
Creating table.
 Done.
...
Table does not exist.
{% endblockquote %}

查看代码，发现是example code里的错误

![code](/images/post/2016-08-26-code1.png)

## 关于`table.modifyFamily()`

* `table.modifyFamily()` 如果column-family不存在时， 会抛exception
* `admin.modifyTable()` 运行之后table里只剩下传递参数HTableDescriptor中指定的那些列了，所以需要先从HBase里查询一次。

修改column-family的代码：

{% codeblock lang:java %}
// Update existing column family
// HTableDescriptor table = new HTableDescriptor(tableName);
HTableDescriptor table = admin.getTableDescriptor(tableName);

HColumnDescriptor existingColumn = new HColumnDescriptor(CF_DEFAULT);
existingColumn.setCompactionCompressionType(Compression.Algorithm.GZ);
existingColumn.setMaxVersions(HConstants.ALL_VERSIONS);
table.modifyFamily(existingColumn); //=> will throw exception: Column family does not exist
//table.addFamily(existingColumn);
admin.modifyTable(tableName, table);
{% endcodeblock %}
