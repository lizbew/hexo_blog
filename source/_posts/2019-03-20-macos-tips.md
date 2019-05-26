---
title: macos使用小技巧
date: 2019-03-20 21:14:47
tags: [macos]
---

## Mac 录制App操作动画及音频

曾经帮助LH录制过APP的操作演示， 研究了下Mac的相关工具。 很久之前的事情，回忆记录。 演示APP的有动画及音频输出， 录屏在Mac下有现成的工具， 音频才是难点，如果直接外放录音会记录下周围的噪音，比如隔壁小孩子的说话声。

* 录屏使用Mac自带的QuickTime Player, 支持全屏录制及选择区域的录制
* APP的音频的录制需要安装软件[Soundflower](https://github.com/mattingalls/Soundflower)，实现一个虚拟的音频输出设备，将系统的音频转发到另一个应用。在使用QuickTime Player录屏时可以使用该设备作为音频来源， 不会混入周围的噪音。 不方便的一点就是， 在录屏过程中你是听不到应用的任何声音的。


