---
layout: post
title: "Build Docker image with packer"
description: "packer is one automation tool to build machine images. Thia article use it to build docker image"
category: tool
tags: [docker, packer]
---

Packe是构建系统镜像的自动化工具，支持多种平台， 比如 Amazon CE2, DigitalOcean, VirtualBox, VMWare, 也支持Docker。 构建Docker image时， 不需要Dockerfile， 所需安装的软件都是通过Provision实现。Packer的配置文件都是写在一个JSON文件里的。

* [packer.io](https://packer.io/)
* [Packer in github.com](https://github.com/mitchellh/packer)

Packer的组件:

* Builder - 对应于不同的平台， 比如VirtualBox的builder, Docker的builder
* Provisioner - 配置image, 比如安装软件包
* Post-processor - 对生成image的后继操作，比如docker-commit, deploy

## Packer的命令行

[packer.io](https://packer.io/)提供了不同平台的预编译包， 下载即可。 Linux AMD64的zip包中有83M, 包含多个工具，每个有近9M。

    $ /usr/local/packer/packer
    usage: packer [--version] [--help] <command> [<args>]
    
    Available commands are:
        build       build image(s) from template
        fix         fixes templates from old versions of packer
        inspect     see components of a template
        push        push template files to a Packer build service
        validate    check that a template is valid
        version     Prints the Packer version

packer命令看起来很简单的。 [INTRODUCTION TO PACKER](https://packer.io/intro)里使用的构建分二步。

* `$ packer validate example.json`
* `$ packer build example.json`

## 用Packer来构建Docker image

先来看看`docker_redis.json`的内容。 当然， 需要构建Docker image的话，也需要安装Docker.

    {
        "builders": [
            {
                "type": "docker",
                "image": "ubuntu",
                "commit": true
            }
        ],
        "provisioners": [
            {
                "type": "shell",
                "inline": [
                    "sleep 30",
                    "sudo apt-get install update",
                    "sudo apt-get install -y redis-server"
                ]
            }
        ],
        "post-processors": [
            {
                "type": "docker-tag",
                "repository": "redis-test",
                "tag": "packer"
            }
        ]
    }

整个JSON内容就分为三块。 `builders`时指定type为docker, 而 base image 为ubuntu。`"commit":true`指定需要运行`docker commit`， 由container生成image. `provisioners`将运行一个shell, 安装redis-server。 最后，在`post-processors`里为image 添加tag `redis-test:packer`.

    $ packer validate docker_redis.json
    $ packer build docker_redis.json
    $ packer images redis*

