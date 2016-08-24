---
layout: post
title: "从jar里查找java class"
description: ""
category: python
tags: [python, script, java, class, ClassNotFound]
---

从命令行运行java程序时遇到ClassNotFound, classPath里少include一些jar包。lib目录下有太多的jar了，不知道到底缺少哪个，便写了个脚本遍历文件夹下所有jar来查找class。

{% codeblock lang:python %}
#!/usr/bin/env python
# -*- coding:utf-8 -*-

# findJarClass.py

import os
import zipfile

def mapToFile(className):
    return className.replace('.', '/') + '.class'

def handleWalkError(err):
    print 'Error When Access ', err.filename
    print err

def findJarInDir(dir_root, className):
    classPath = mapToFile(className)
    for root, dirs, files in os.walk(dir_root, onerror=handleWalkError):
        if not files:
            continue
        for f in files:
            if f.lower().endswith('.jar'):
                fpath = os.path.join(root, f)
                with zipfile.ZipFile(open(fpath, 'rb')) as zf:
                    if classPath in zf.namelist():
                        print fpath

findJarInDir(r'D:\Oracle\Middleware', 'weblogic.Deployer')
{% endcodeblock %}

