---
layout: post
title: "Install Archlinux in Mele A100"
description: "Hack Mele A100, install ArchLinux in SD card and also LXDE GUI environment"
category: "Linux"
tags: [MeleA100, Linux, ArchLinux]
---

Linux 部分主要按[archlinuxarm.org](http://archlinuxarm.org/platforms/armv7/mele-a100)上的步骤来的。安装后就能从SD卡启动，并且可以通过SSH远程登录；但要连接Mele A100的VGA到显示器，却费了些周折。

了解Mele A100
=============

Mele A10原本只是一个Android 视频播放器，但因接口丰富，支持从SD卡启动，且有较高的性价比，已经被老外拿来各种折腾了。Mele A100的核心是珠海全志科技(Allwinner)的A10 Soc芯片，基于ARM Cortex-A8,单核1.0Ghz, 集成Mali 400 GPU. Mele A100最初上市是512M内存，最近已经升级到1G了。以下是摘自Archlinuxarm.org:

    ARM® Cortex-A8 1.0Ghz
    MALI400MP OpenGL ES 2.0 GPU
    HDMI, VGA, Component Video
    HDMI, SPDIF Audio
    3 USB 2.0
    IR Remote
    SD 3.0, UHI class


安装Linux文件系统到SD卡
======================

首先需要准备一张空白的SD 卡，格式化并分区，再安装linux根文件系统。我是借用了相机的4G SD card, 所有步骤都是在openSUSE下进行的。

SD 分区
-------

有现成的script mkA10card.sh完成分区，下载[Mele bootloader tarball](http://archlinuxarm.org/os/sun4i/Mele-bootloader.tar.gz), 解压后得到mkA10card.sh。Script会将SD卡划分成两个分区：第一个为16 MB FAT, 另一个为ext4。当连接SD卡后，新加载的设备在我的系统中显示为/dev/sda.

{% codeblock lang:bash %}
wget http://archlinuxarm.org/os/sun4i/Mele-bootloader.tar.gz
tar xzf Mele-bootloader.tar.gz
./mkA10card.sh /dev/sdX
{% endcodeblock %}

直接使用下载的mkA10car.sh会有点小问题，会发现给boot分区分配了有接近2G的空间，而建议的是16M的就足够了。要将mkA10car.sh有的小改动。sfdisk分区时以Cylinder为单位， 使用默认值一个Cylinder大约是3M。下载的script中第1分区从第32 Cylinder开始，占用接下来的512个Cylinder, 空间占用将大于1.5G。新的分区方式是从第1 Cylinder开始，占用6个Cylinder, 约18M。运行mkA10car.sh时会打印出Cylinder相关的设置， `1 cylinder = 122(heads) * 62 (sectors) * 512B`。

找到如下内容

{% codeblock lang:bash %}
# ~2048, 16MB, FAT, bootable
# ~rest of drive, Ext4
{
echo 32,512,0x0C,*
echo 544,,,-
} | sfdisk -D $DRIVE
{% endcodeblock %}

修改为

{% codeblock lang:bash %}
# ~2048, 16MB, FAT, bootable
# ~rest of drive, Ext4
{
echo 1,6,0x0C,*
echo 7,,,-
} | sfdisk -D $DRIVE
{% endcodeblock %}

当分区完成后，可看到新分区显示为`/dev/sda1`和`/dev/sda2`。Git [u-boot-sunxi](https://github.com/linux-sunxi/u-boot-sunxi/wiki) wiki上storage map:

{% codeblock %}
start size
  0   8KB Unused, available for partition table etc.
  8  24KB Initial SPL loader
 32 512KB u-boot
544 128KB environment
 672 352KB reserved
1024    - Free for partitions
{% endcodeblock %}

安装root filesystem
-------------------

下载[the root filesystem tarball](http://archlinuxarm.org/os/ArchLinuxARM-sun4i-latest.tar.gz)，并以root身份将压缩包解压到SD卡的ext4分区。

{% codeblock lang:bash %}
mkdir /tmp/boot
mkdir /tmp/arch
mount /dev/sda1 /tmp/boot 
mount /dev/sda2 /tmp/arch
wget http://archlinuxarm.org/os/ArchLinuxARM-sun4i-latest.tar.gz
tar -zxf ArchLinuxARM-sun4i-latest.tar.gz -C /tmp/arch
cp /tmp/arch/boot/uImage /tmp/boot/uImage
cp script.bin /tmp/boot/script.bin
cp uEnv.txt /tmp/boot/uEnv.txt
{% endcodeblock %}

从SD卡启动Mele A100
-------------------

从电脑卸载SD卡，插入Mele A100后，连接电源，就可以按开机键启动了。现在连接显示器是没有任何输出的，还没有加载显示驱动模块。

{% codeblock lang:bash %}
sync
umount /dev/sda*
{% endcodeblock %}

