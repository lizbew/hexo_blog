---
layout: post
title: "VirtualBox network modes and Vagrant configure"
description: "There are 4 network modes in Virutalbox, and you can configure in Vagrant easily"
category: tool
tags: [virtualbox, vagrant, network]
---

There are 4 network modes in virtualbox.

- Network Address Translation(NAT), the simplest way. Guest OS can access network, but other machines cannot access the Guest OS.  You need port-forwarding to export service in guest-os to others.
- Bridged networking - Same level as the host machine in the network
- Internal networking - multiple guest OSs can access each other, and the host machines and others cannot access. Guest OSs are in one virtual private network.
- Host-only, smilar to Internal networking, but the host machine can access.


I need to startup 2 CentOS in virtualbox, and they can access each other, in order to test Zabbix. Host-only network is needed.

## Configuration in Vagrantfile

    config.vm.network "forwarded_port", guest: 80, host: 8080
    config.vm.network "private_network", ip: "192.168.33.10"

Vagrant will setup NAT network by default, and forwarded port 22 for SSH.  More ports are forwarded by `config.vm.network "forwarded_port", guest: 80, host: 8080`. 

`config.vm.network "private_network", ip: "192.168.33.10"` will create Host-only network, and with IP 192.168.33.10. You neeed to special different private network IP for each guest OS, then can use this IP to access each other. 

## Reference

- [Vagrant Networking](https://docs.vagrantup.com/v2/networking/index.html)

