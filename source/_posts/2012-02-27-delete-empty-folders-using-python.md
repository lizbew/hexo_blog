---
layout: post
title: "Delete empty folders using Python"
description: ""
category: python
tags: [python, script]
---

{% codeblock lang:python %}
import os, os.path
import stat
 
BASE_FOLDER = r'C:\MessageStorage'
 
fl = os.listdir
 
def delFolder(folder):
    fl = os.listdir(folder)
    #print fl
    if len(fl) == 0:
        os.rmdir(folder)
        print "deleted folder"
        return;
    else:
        os.chdir(folder)
        for f in fl:
            if os.path.isdir(f):
                delFolder(os.path.join(folder, f))
        os.chdir('..')
        fl = os.listdir(folder)
        if len(fl) == 0:
            os.rmdir(folder)
            print "deleted folder"
 
delFolder(BASE_FOLDER)

{% endcodeblock %}
