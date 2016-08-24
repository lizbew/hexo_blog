---
layout: post
title: "Run Local Docker Registry"
description: "Start docker registry in local server, then can push/pull from it"
category: tool
tags: [docker, docker-registry]
---

本文的主要内容来自于Docker Docs的两篇文章

* [Run a local registry mirror](https://docs.docker.com/articles/registry_mirror/)
* [Deploying a registry server](https://docs.docker.com/registry/deploying/)

Registry的Dockerfile

* [https://registry.hub.docker.com/_/registry/](https://registry.hub.docker.com/_/registry/)

## Run a local registry mirror

第一次从local registry mirror读取image时， 它会先从公共的Docker registry取得image， 并存于在本地； 在随后的接收到的相同的image request时，会将本地存储的image返回。

运行local registry mirror需要分两步走。 

### 配置Docker daemons

可以要启动docker daemon时从命令行指定registry_mirror。 ubuntu下docker daemon是由Upstart管理的， 会随机器启动时运行， 就需要先停下了。

    $ sudo stop docker
    $ sudo docker --registry-mirror=http://<my-docker-mirror-host> -d

或者是写入配置文件`/etc/default/docker`， 将`--registry-mirror`添加在值`DOCKER_OPTS`后面。

### 启动local registry mirror

直接使用官方提供的`registry` image即可。 当前最新的版本是`registry:2.0`， 不过`registry:latest` 好像是指向版本0.9的。启动后使用端口`5000`.

    sudo docker run -p 5000:5000 \
        -e STANDALONE=false \
        -e MIRROR_SOURCE=https://registry-1.docker.io \
        -e MIRROR_SOURCE_INDEX=https://index.docker.io \
        registry

## 将image提交到local registry

其实很简单的， 将image添加标签`[REGISTRYHOST/]NAME[:TAG]`即可。 更多内容与细节请参考[Deploying a registry server](https://docs.docker.com/registry/deploying/)。

    $ docker tag hello-world:latest localhost:5000/hello-mine:latest
    $ docker push localhost:5000/hello-mine:latest
    $ curl -v -X GET http://localhost:5000/v2/hello-mine/tags/list

先将image `hello-world:latest` 打上标签 `localhost:5000/hello-mine:latest`， 再push. 通过访问[http://localhost:5000/v2/hello-mine/tags/list](http://localhost:5000/v2/hello-mine/tags/list) 进行确认。

