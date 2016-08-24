---
layout: post
title: "用python批量替换command文件中的字符串"
description: "用python实现脚本，替换文件下所有command文件里的字符串"
category: python
tags: [python, script]
---

移动了一个Weblogic的安装目录后，发现有很多command文件里的路径需要更改，于是就有了下面的python script。实现非常简单，运行前先该路径和替换字符串，只能简单的文本替换，且在遇到hiden文件时有perssion error.

文件名为replaceCmdstr.py

{% codeblock lang:python %}
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

def updateFileContent(fpath, old, new):
    content = open(fpath, 'rb').read()
    if old in content:
        open(fpath, 'wb').write(content.replace(old, new))
        print 'Updated', fpath
    

def handleWalkError(err):
    print 'Error When Access ', err.filename
    print err

def updateFilesinDir(dir_root, old_str, new_str, exts = ['.cmd', '.bat']):
    for root, dirs, files in os.walk(dir_root, onerror=handleWalkError):
        if not files:
            continue
        for f in files:
            bname, ext = os.path.splitext(f)
            if ext in exts:
                fpath = os.path.join(root, f)
                updateFileContent(fpath, old_str, new_str)

updateFilesinDir(r'D:\Oracle\Middleware', r'C:\Oracle', r'D:\Oracle')
{% endcodeblock %}
