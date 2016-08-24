---
layout: post
title: "Docker cannot connect to external network"
description: "some information when I resovle Docker cannot connect to internet"
category: tool
tags: [docker, network]
---

昨天build docker时遇到连接网络失败的问题，折腾了一番后还是不行。 但是今天重启后再试时，又没问题了。所以具体的是什么问题引起的话，就没法确认了，不过最有可能是DNS的问题。 Container打印出的error log为下面内容。

    npm ERR! fetch failed https://r.cnpmjs.org/cross-spawn/download/cross-spawn-0.2.9.tgz
    npm WARN retry will retry, error on last attempt: Error: getaddrinfo ENOTFOUND r.cnpmjs.org
    npm ERR! fetch failed https://r.cnpmjs.org/open/download/open-0.0.5.tgz

## 安装Docker的可选配置

首先是重新看了一遍Docker Installion Guide, 将可选的一些操作试了一次。 [Optional Configurations for Docker on Ubuntu](https://docs.docker.com/installation/ubuntulinux/#optional-configurations-for-docker-on-ubuntu).

### 新建用户组 docker

运行docker需要root权限，每一次命令都需要加sudo, `sudo docker ...`。当前当前用户添加docker组后， `docker`会在docker组下运行， 就不需要再用sudo了。 其实docker组和root组是相同的。

    $ sudo usermod -aG docker ubuntu
    $ docker run hello-world

### Adjust memory and swap accounting

编辑`/etc/default/grub`， 设置`GRUB_CMDLINE_LINUX`的内容为如下， 并保存内容

    GRUB_CMDLINE_LINUX="cgroup_enable=memory swapaccount=1"

再更新grub设置

    $ sudo update-grub

### Enable UFW forwarding
  
本人机器上`ufw`的是`inactive`就没做调整。不过是记录下相关步骤。

    $ sudo ufw status
    $ sudo nano /etc/default/ufw
    DEFAULT_FORWARD_POLICY="ACCEPT"
    $ sudo ufw reload
    $ sudo ufw allow 2375/tcp

### Configure a DNS server for use by Docker

查看后发现`nameserver 127.0.0.1`在文件`/etc/resolv.conf`里。 我采用是设置docker的`DOCKER_OPTS`:

    $ sudo nano /etc/default/docker
    DOCKER_OPTS="--dns 8.8.8.8"
    $ sudo restart docker

另一种方式是停用`dnsmasq`:

    $ sudo nano /etc/NetworkManager/NetworkManager.conf
    # dns=dnsmasq
    $ sudo restart network-manager
    $ sudo restart docker

## Docker 网络设置

  * [Network Configuration](https://docs.docker.com/articles/networking/)
  * [中文翻译](http://www.oschina.net/translate/docker-network-configuration)
  * [利用iptables实现docker网关路由及内网服务端口映射](http://www.xiaomastack.com/2015/03/28/iptables-docker/)

运行Docker的主机上会建立`docker0`的桥接，和类似`vethAQI2QT`的虚拟网卡, 进出Docker Container的数据包都需要经过`docker0`.

查看网卡信息。 排查container问题时，可以使用`$ ifconfig docker0`查看经过的数据包数量，被拒数量，和总大小。在`docker build`过程中，需要下载文件包，如果长时间没信息打印出，可查看`docker0`的数据总量大小是否有变化。

    $ ifconfig -a
    $ ifconfig docker0
    $ ip addr
    $ ip route
    $ docker run -ti --rm node:0.12 ping -c 4 8.8.8.8

IP包转发，`ip_forward`:

    $ sysctl net.ipv4.conf.all.forwarding
    net.ipv4.conf.all.forwarding = 0
    $ sysctl net.ipv4.conf.all.forwarding=1
    $ sysctl net.ipv4.conf.all.forwarding
    net.ipv4.conf.all.forwarding = 1

查看iptables设置 

    $ sudo iptables -L -n
    $ sudo iptables -t nat -L -n

Container DNS, 三个文件： `/etc/hostname`, `/etc/hosts`, `/etc/resolv.conf`

    $ mount
    ...
    /dev/disk/by-uuid/1fec...ebdf on /etc/hostname type ext4 ...
    /dev/disk/by-uuid/1fec...ebdf on /etc/hosts type ext4 ...
    /dev/disk/by-uuid/1fec...ebdf on /etc/resolv.conf type ext4 ...
    ...

