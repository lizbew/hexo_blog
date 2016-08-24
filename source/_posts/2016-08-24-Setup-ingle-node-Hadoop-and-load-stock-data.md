---
title: Setup ingle-node Hadoop and load stock data
date: 2016-08-24 15:53:07
tags:
- Hadoop
- HDFS
---

# 搭建单节点Hadoop,  加载股票数据到HDFS

使用的环境为Ubuntu 16 64/位系统。

## 环境搭建

首先参照Hadoop的[官方文档](http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/SingleCluster.html)搭建单节点的系统。 如下修改configuration文件， NameNode为localhost:9000。

* etc/hadoop/core-site.xml
```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```

* etc/hadoop/hdfs-site.xml
```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>
```

在Bash 下运行命令：

```bash
$ bin/hdfs namenode -format
$ sbin/start-dfs.sh
$ sbin/stop-dfs.sh # stop deamons
```

## 上传股票数据到HDFS

股票数据来源为网易财经， 运行一个python script将所有股票的最新价格保存为一个文件， 文件名以日期命名， 形如`2016-08-21.csv`。

python script: [save_price_daily_csv.py](/files/save_price_daily_csv.py)

使用Hadoop提供的工具将生成的csv保存到HDFS:

```bash
$ bin/hdfs dfs -mkdir -p /user/vagrant/stock-daily-price
$ bin/hdfs dfs -put /vagrant/tmp/2016-08-21.csv stock-daily-price/
```

## 统计涨跌数的MapReduce程序

参考Wordcount的代码， 依葫芦画瓢， 写出下面一段代码， 添加hadoop相关的jar包，编译打包成`HapTet-1.0-SNAPSHOT.jar`. 代码部分只需要重写`map()`函数即可。


```bash
$ bin/hadoop jar /vagrant/tmp/HapTet-1.0-SNAPSHOT.jar com.viifly.hadoop.ta1.StockCount stock-daily-price/2016-08-21.csv out/
$ bin/hdfs dfs -cat ./out/*
```


```java
package com.viifly.hadoop.ta1;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class StockCount {
    public static final String UP3 = "UP3";
    public static final String UP0 = "UP0";
    public static final String DW0 = "DW0";
    public static final String DW3 = "DW3";

    public static class TokenizerMapper
            extends Mapper<Object, Text, Text, IntWritable>{

        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();

        public void map(Object key, Text value, Context context
        ) throws IOException, InterruptedException {
            /*
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken());
                context.write(word, one);
            }
            */
            String line = value.toString();
            String[] fields = line.split(",");
            if (fields.length > 5 && (fields[0].charAt(0) == '0' || fields[0].charAt(0) == '6' )) {
                Float percent = Float.parseFloat(fields[3]) * 100;

                String t = null;
                if (percent >= 3) {
                    t = UP3;
                } else if (percent >= 0) {
                    t = UP0;
                } else if (percent >= -3) {
                    t = DW0;
                } else {
                    t = DW3;
                }
                word.set(t);
                context.write(word, one);
            }
        }
    }

    public static class IntSumReducer
            extends Reducer<Text,IntWritable,Text,IntWritable> {
        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values,
                           Context context
        ) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Stock Count");
        job.setJarByClass(StockCount.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

```
