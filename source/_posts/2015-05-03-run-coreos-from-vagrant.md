---
layout: post
title: "Run coreos from Vagrant"
description: "Vagrant is management tools for virtualbox, will use it to restart coreos VM"
category: tool
tags: [coreos, vagrant, docker, virtualbox]
---

VAGRANT是虚拟机管理工具，可以方便的添加和启动虚拟机； CoreOS是专为docker而设计的系统， 每一个应用都运行在docker环境下。 当VAGRANT + CoreOS时，你就可以很容易在windows下体验学习docker；虽然可以使用Boot2docker，但是多了一个选择， 且CoreOS文档也支持在VAGRANT下运行。

* VAGRANT: [https://www.vagrantup.com/downloads.html](https://www.vagrantup.com/downloads.html)
* CoreOS: [https://coreos.com/docs/running-coreos/platforms/vagrant/](https://coreos.com/docs/running-coreos/platforms/vagrant/)
* Boot2docker: [http://boot2docker.io/](http://boot2docker.io/)

## VAGRANT

VAGRANT支持virtualbox 和VMWare的虚拟机，默认是virtualbox。 如果使用VMWare的虚拟机，需要在Vagrantfile里指定，详情可参考 VAGRANT官方文档。 在安装VAGRANT之前， 要先安装好virtualbox。

VAGRANT下的虚拟机image称为`box`, 在启动虚拟机之前， 需要先添加`box`。 VAGRANT有像Docker HUB一样的Box Repository， 如下 `vagrant box add` 命令中的<url> 可以使用`USER/BOX`的形式，如`hashicorp/precise32`， VAGRANT会从repository下载。

    $ vagrant box add <title> <url>     # 添加box
    $ vagrant init <title>              # 生成 Vagrantfile
    $ vagrant up                        # 启动虚拟机
    $ vagrant ssh                       # ssh 连接到虚拟机

启动/停止相关的命令：

    $ vagrant up
    $ vagrant halt
    $ vagrant suspend
    $ vagrant resume
    $ vagrant destroy

box相关的命令：

    $ vagrant box list
    $ vagrant box remove <name>
    $ vagrant reload <vm-name>

### Vagrantfile

`vagrant init <title>` 会在当前路径下生成`Vagrantfile`， 保存了虚拟机的配置信息， 后续命令都会使用到文件。 只说点重要的。

* 网络配置相关

      config.vm.network :forwarded_port, guest: 80, host: 8080
      config.vm.network :public_network
      config.ssh.forward_agent = true

* 共享文件夹映射

      config.vm.synced_folder "../data", "/vagrant_data"

* provision

      config.vm.provision :shell, :path => "boot.sh"

## CoreOS

我是跟着文档 [Running CoreOS on Vagran](https://coreos.com/docs/running-coreos/platforms/vagrant/) 开始的。

    $ git clone https://github.com/coreos/coreos-vagrant.git
    $ cp config.rb.sample config.rb
    $ cp user-data.sample user-data

在`user-data`里有一处需要改动，先找到如下的行，有两处，只需要取消一行前的注释符`#`即可。`user-data`是YML格式的文件， 需要取消注释的是`etcd`下的，因为默认是启动服务项`etcd.service`。 如果要换成启动`etcd2.service`， 那就相应的取消`etcd2`下的`discovery`。

    #discovery: https://discovery.etcd.io/<token>

然后再将`<token>`换成从[https://discovery.etcd.io/new](https://discovery.etcd.io/new)返回的结果。

接下来， 就可以启动CoreOS虚拟机了。 正常情况下会自动下载box， 但是网络环境的问题， 会出现域名无法解析的问题， 下载coreos box失败。*需要自备梯子了*。

    $ vagrant up

本人是在通过另外的网络下载了coreos_production_vagrant.box， 使用了稳定的版本， 需要改动`config.rb`里的`$update_channel='stable'`。 在启动之前就需要手动先添加box了。

    $ vagrant box add coreos-stable ../boxes/coreos_production_vagrant.box
    $ vagrant up
    $ vagrant ssh

准备就绪， 就可以开始 docker之路了

    $ docker pull ubuntu:latest
    $ docker images
    $ docker run -t -i ubuntu:latest /bin/bash

