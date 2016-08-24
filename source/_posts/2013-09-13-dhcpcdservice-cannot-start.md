---
layout: post
title: "dhcpcd.service不能启动"
description: ""
category: linux
tags: [linux, systemctl]
---

原始发布于： http://blog.viifly.com/blog/posts/5865619656278016

一个运行Archlinux ARM版的mele A100播放器每次启动后都不能访问网络，必须手动运行dhcpcd命令。最开始查找/etc/init.d/下service启动脚本，但是根本就没有/etc/init.d/这个文件夹。通过ArchLinux的wiki才知道要用命令**systemctl**来控制service。运行systemctl会显示出所有service的状态，发现有两行红色出ACTIVE为failed: netcfg.service和dhcpcd@eth0.service。

今天参看了Archlinux的wiki来了解[systemd][1]， 试图解决dhcpcd@eth0.service启动失败的原因。虽然现在还不清楚 failed的原因，但至少知道来查看log， 并让两个service都启动起来了。systemd的unit文件位于**/usr/lib/systemd/system/** 和 __/etc/systemd/system/__。

 - 列出failed的service:

    $ systemctl --failed
    $ systemctl status dhcpcd@eth0.service

![systemctl status](/images/post/systemctl_status.png)

 现在看到的只有一个failed, 这是后来手动运行`dhcpcd`命令，网络连接正常后用ssh连接再截的图。`# systemctl restart netcfg`一次就将netcfg.service启动成功，但对dhcpcd@eth0.service就不那么好使了，试了几次都不成功，最后只好手动`dhcpcd`命令了。但当网络连接好后再次使用`# systemctl restart dhcpcd@eth0.service`就可以成功。 真是奇怪。

***
 - 查看systemd log

systemd 使用的log 系统为**journal**， log文件的位置为/var/log/journal/，而配置在/etc/systemd/journald.conf。查看journal log的命令为journalctl。

    # journalctl -xn
    # journalctl -u netcfg
    # journalctl -b

  [1]: https://wiki.archlinux.org/index.php/Systemd_%28%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87%29
