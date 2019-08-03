---
title: 初识 link
date: 2019-08-03 20:32:41
tags: [flink]
---

这两天看了InfoQ网站上 "Apache Flink 零基础入门" 系统文章，学了点皮毛， 记录一下。

## 安装Flink

最简单的方法还是从官网下载二进制，解压之后就可以使用了。刚开始还打算从源代码编译，但遇到包下载不成，折腾了两天的空闲时间还是放弃了。 下载连接 https://flink.apache.org/zh/downloads.html 


## 启动、停止

Flink支持单机集群Standalone, 多机集群及基于 Yarn 调度系统。 个人测试使用Standalone, 如下命令启动后，浏览器访问 http://localhost:8081

```bash
# 启动集群
./bin/start-cluster.sh
# 提交运行示例程序
./bin/flink run -d ./examples/streaming/TopSpeedWindowing.jar
# 查看job命令列表
./bin/flink list -m localhost:8081
# stop/cancel job
./bin/flink cancel -m localhost:8081 cdc611aec41844019bec2058a616accb
```

停止集群使用如下命令：

```bash
./bin/start-cluster.sh
```
## JobManager/TaskManager

Flink 在架构上分为 JobManager与TaskManager， JobManager 是任务的控制者，TaskManager 是执行任务的worker， 都是一个JVM. TaskManager 中运行的单位为Task slot, 相当于一个线程。 一个TM默认只有一个task slot， 可以通过修改配置文件`conf/flink-conf.yaml` 中的配置来设置Task slot个数。修改Task slot个数时， savepoint的路径也需要配置， 因为修改job的并发度时要先在savepoint保存状态，在重新调度。

```yml
# vim ./conf/flink-conf.yam
taskmanager.numberOfTaskSlots: 4
state.savepoints.dir: file:///tmp/savepoint
```

如果命令来修改并发度(使用task slot个数)：

```bash
./bin/flink modify -p 4 -m localhost:8081 2d75b06069f5319b909d4150ad3ae7df
```

## 下一步

现在只体验了命令行， 还没有自己写代码。 下一步希望自己实现flink简单任务，与kafka connector集成，然后深入了解window, extact-once语义。

## 参考

* [Flink](https://flink.apache.org/zh/)
* [Apache Flink 零基础入门（五）](https://www.infoq.cn/article/WCOvi-D68Y8ycCiYZ8pX)  这个里包含对前几个文章的索引
* [Apache Flink 零基础入门（六）](https://www.infoq.cn/article/VGKZA-S9fMBgABP71Pgh)
* [如何利用开源 Flink 和 Pravega 搭建完整的流处理架构？](https://www.infoq.cn/article/jBo_6AYG4IViKkiHusgB)
* [Flink Kafka Connector 与 Exactly Once 剖析](https://www.infoq.cn/article/58bzvIbT2fqyW*cXzGlG)
* [Flink Slot 详解与 Job Execution Graph 优化](https://www.infoq.cn/article/ZmL7TCcEchvANY-9jG1H)