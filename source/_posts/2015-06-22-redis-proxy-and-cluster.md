---
layout: post
title: "Redis安装及代理与集群"
description: "Redis是简单易用的内存缓存，支持多种数据类型及其操作"
category: 
tags: [redis, twemproxy, codis]
---

最近使用了redis, 然后开始了解redis集群方案。比较出名的是以下三种了，twemproxy和codis是代理； 而Redis Sentinel则是集群，管理redis的fail over.

- twemproxy
- codis
- Redis Sentinel

## 安装 Redis

从源码安装Redis已经是非常简单了。最新的源码包是3.0的了，[下载页面](http://redis.io/download)。

{% codeblock lang:bash %}
$ wget http://download.redis.io/releases/redis-3.0.2.tar.gz
$ tar xzf redis-3.0.2.tar.gz
$ cd redis-3.0.2
$ make
$ sudo make install
{% endcodeblock %}

redis提供现成的工具来添加新的redis 实例，可以自动生成cofing和init script. 

{% codeblock lang:bash %}
$ sudo ./utils/install_server.sh
$ sudo service redis_6379 status
{% endcodeblock %}

然后就可以使用redis客户端工具来访问redis了：

{% codeblock lang:bash %}
$ redis-cli -p 7379
redis> set foo bar
redis> get foo
{% endcodeblock %}


## 安装 twemproxy

twemproxy 是twitter出品的memcached和redis的proxy, 项目开源在[github](https://github.com/twitter/twemproxy)。

个人是尝试安装了， 并无太深入的研究, 简单记录下过程。


{% codeblock lang:bash %}
$ sudo yum install autoconf automake libtool
$ git clone https://github.com/twitter/twemproxy.git
$ cd twemproxy
$ autoreconf -fvi
$ ./configure --enable-debug=full
$ make
$ src/nutcracker -h
{% endcodeblock %}

twemproxy编译后生成的二进制文件为nutcracker， 使用默认的配置文件为`conf/nutcracker.yml`。本人重新添加的一个新的配置文件， my-nutcracker.yml， 运行一个twemproxy实例， redis的实例为2个。 具体内容如下：

{% codeblock lang:yaml %}
alpha:
  listen: 127.0.0.1:22121
  hash: fnv1a_64
  distribution: ketama
  auto_eject_hosts: true
  redis: true
  server_retry_timeout: 2000
  server_failure_limit: 1
  servers:
    - 127.0.0.1:6379:1
    - 127.0.0.1:6380:1
{% endcodeblock %}

twemproxy监听的端口为22121， 可以使用redis客户端来连接了， 如同连接一个redis端口。

{% codeblock lang:bash %}
$ redis-cli -p 22121
> set k1 a
{% endcodeblock %}

## Codis

还没试过Codis，再补上。 https://github.com/wandoulabs/codis

InfoQ 上有个视频讲解Codis实现的： http://www.infoq.com/cn/presentations/design-and-implementation-of-wandoujia-distributed-redis。

