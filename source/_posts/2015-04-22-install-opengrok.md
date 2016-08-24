---
layout: post
title: "install opengrok"
description: "steps to install opengrok, a opensource code cross reference tool"
category: tool
tags: [opengrok, tomcat, xref, ctags]
---

试着安装了OpenGrok， 将感兴趣的开源项目源代码交叉索引后，方便阅读代码。在此记录步骤，只想表明曾经做过这么件事。

* [OpenGrok](https://github.com/OpenGrok/OpenGrok/wiki/How-to-install-OpenGrok)

安装使用的机器为ubuntu server 12.x, 安装路径为`/srv/opengrok`, 源代码放于OpenGrok默认的路径`/var/opengrok/src`下。


## 安装tomcat

使用了tomcat 8.0，具体细节不多说了。新建文件bin/setenv.sh，内容如下。 配置完成后启动tomcat.

    JRE_HOME=/usr/lib/jvm/java-7-openjdk-amd64/jre

## 安装ctags

* Download: [ctags](http://ctags.sourceforge.net/)

从源码安装ctags, 两步搞定

    make && sudo make install


## OpenGrok

将下载的OpenGrok软件包解压于/srv/opengrok， 启动脚本`OpenGrok`部署到tomcat下，需要指定tomcat的安装路径。

    cd /srv/opengrok/opengrok-0.12.1/bin
    OPENGROK_TOMCAT_BASE=/srv/opengrok/apache-tomcat-8.0.21 ./OpenGrok deploy

新建路径用于存放源代码及OpenGrok数据, 即OpenGrok手册中所说的SRC_ROOT和DATA_ROOT.

    sudo mkdir -p /var/opengrok/src
    sudo chown user:group /var/opengrok
    mv ctags-5.8  /var/opengrok/src

然后就是索引源码 

    cd /srv/opengrok/opengrok-0.12.1/bin
    ./OpenGrok index

打开浏览器， 进入tomcat所使用端口， 在路径`http://localhost:8080/source/xref`下就可以看到索引的项目了。

## 添加新的代码到索引

1. 将解压缩过后的代码文件移到到`/var/opengrok/src`下，推荐的文件夹命名方式为`name-version-branch`
2. 运行命令`/srv/opengrok/opengrok-0.12.1/bin/OpenGrok index`

## 索引时OutOfMemory

JVM下遇到是经常的事， 当添加几个项目后跑`OpenGrok index`就遇到了。

    09:18:33 SEVERE: Problem updating lucene index database:
    java.lang.OutOfMemoryError: Java heap space

加大Heap Size就解决了

    JAVA_OPTS=-Xmx3072m ./OpenGrok index

