---
layout: post
title: "替换smali文件中被混淆的类名"
description: "use python to implement a tool to replace class name in smali files"
category: python
tags: [python, script, smali, android]
---

将Android程序包（apk文件）中的classes.dex反汇编成smali文件后，看到整个文件夹下都是a,b,c..smali这样的被混淆过的文件名就想要放弃了；可用文本编辑器打开一个smali文件，看到第三行`.source xxx.java`时，顿时感到生活还是很有希望的。如果将samli中的class名能替换成.source所提示的名字，看反编译后的java code的痛苦度就会少个零了。主要考虑使用Python来实现。

![2.png](/images/post/2014-11-27/2.png)

## 0x00 想法

smali文件的前三行通常都是.class/.super/.source, 可以先读取所有smali文件，生成一个从原始class name到新class name的映射；然后再遍历每一个smali文件，查找内容中的类似`Lcom/xx/xxx;`的类名，如果在上一步生成的映射里就用新的类名替换；如果某个smali文件所代表的类有变化，还要相应重命名文件。

## 0x01 遇到的问题

### smali文件中`.source`行不存在，或是dummy

* 如果`.source`行不存在，就不用放在class name映射里， 直接跳过
  ![1.png](/images/post/2014-11-27/1.png)
* 发现有些文件为`.source "SourceFile"`, 显然是假的。正常的是以`.java`结尾。这也是需要跳过的情况

  ![4.png](/images/post/2014-11-27/4.png)

### 新的class name生成规则

最简单的情形是将class names最后一个`/`分隔符后的字符串换成`.source "xxx.java"`中去掉后缀`.java`后的`xxx`. 但需要考虑新生成的class name冲突，或是新的smali文件名重复。有下面的情形：

* class name中已经有`$`, 则只需要替换`$`之前的部分
  ![3.png](/images/post/2014-11-27/3.png)
* 多个smali文件的`.source` 内容相同。猜测可能是同一个java文件中定义了嵌套类，生成的class就来自相同的java文件
* 需要重命的新文件名可能已经存在了，且在windows下文件名是大小写敏感的

这里的解决办法是用一个`set`保存所有class name的小写字符串，如过新生成的class name已经存在于set中则在class name 后添加`$`和原始的class name, 如果还是存在则再添加从0-9选出的随机数。在实现过程中调用`os.rename(src,dst)`遇到的`WindowsError: [Error 183]`, 就是因为新文件名已经存在引起的。

## 0x02 Python实现

贴代码最实在了，我用的文件名为`smali_rep.py`。 遍历文件夹中所有smali文件部分，还翻开了[以前的一篇blog](http://healich.iteye.com/blog/1428116), 可惜当初还不会用`os.walk()`。 (._.)

```
# sample usage:
python.exe smali_rep.py ./smali
```

{% codeblock lang:python %}
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import random
import sys

_classMap = {}
_fileClassMap = {}
_reservedClassSet = set()
_re_className = re.compile('L[a-zA-Z_0-9/\$]+;')

def getFilenameSuffix(filename):
    i = filename.rfind('.')
    if i > 0:
        return filename[i:]
    return ''

def convertClassName(cls, sourceName):
    # Landroid/support/v4/app/Fragment;
    segs = cls[1:-1].split('/')
    baseName = segs[-1]
    if '$' in baseName:
        baseName = sourceName + '$' + baseName.split('$', 1)[1]
    else:
        baseName = sourceName
    segs[-1] = baseName
    return 'L'+ '/'.join(segs) + ';'

def getFileNameFromClass(cls, suffix = '.smali'):
    segs = cls[1:-1].split('/')
    return segs[-1] + suffix

def readClassSourceName(smalifd):
    smalifd.seek(0, os.SEEK_CUR)
    cls, source = None, None

    for line in smalifd:
        if len(line.strip('\r\n')) == 0:
            break
        segs = line.split(' ')
        if segs[0] == '.class':
            cls = segs[-1].strip('\r\n')
        elif segs[0] == '.source':
            s = segs[-1].strip('\r\n"')
    return cls, source

def findClassName(smalifile):
    cls, source = None, None
    for line in open(smalifile, 'r'):
        if len(line.strip('\r\n')) == 0:
            break
        segs = line.split(' ')
        if segs[0] == '.class':
            cls = segs[-1].strip('\r\n')
        elif segs[0] == '.source':
            s = segs[-1].strip('\r\n"')
            if s.endswith('.java'):
                source = s[:-5]
    if source is not None:
        newCls = convertClassName(cls, source)
        if newCls != cls:
            _classMap[cls] = newCls
            _fileClassMap[smalifile] = cls
    _reservedClassSet.add(cls.lower())

def clsrepl(matchobj):
    cls = matchobj.group(0)
    if cls in _classMap:
        return _classMap[cls]
    return cls

def updateSmaliContent(smalifile):
    content = open(smalifile, 'rb').read()
    open(smalifile, 'wb').write(_re_className.sub(clsrepl, content))

def renameSmaliFile(smalifile):
    if smalifile in _fileClassMap:
        newCls = _classMap[_fileClassMap[smalifile]]
        newPath = os.path.join(os.path.dirname(smalifile), getFileNameFromClass(newCls))
        try:
            os.rename(smalifile, newPath)
        except Exception as e:
            print smalifile, ' -> ', newPath
            print e
            raise e

def handleWalkError(err):
    print 'Error When Access ', err.filename
    print err

def processSmali(smali_root):
    smali_root = os.path.abspath(smali_root)
    # read class map
    for root, dirs, files in os.walk(smali_root, onerror=handleWalkError):
        if not files:
            continue
        for f in files:
            if f.endswith('.smali'):
                findClassName(os.path.join(root, f))
    # fix duplicate name
    for k in _classMap.keys():
        newCls = _classMap[k]
        if newCls.lower() in _reservedClassSet and '$' not in k:
            newCls = newCls[:-1] + '$' + k[1:-1].split('/')[-1]  + ';'

        while newCls.lower() in _reservedClassSet:
            newCls = newCls[:-1] + str(random.randint(0, 9)) + ';'
        _classMap[k] = newCls
        _reservedClassSet.add(newCls.lower())

    # replace class name
    for root, dirs, files in os.walk(smali_root, onerror=handleWalkError):
        if not files:
            continue
        for f in files:
            if f.endswith('.smali'):
                fpath = os.path.join(root, f)
                updateSmaliContent(fpath)
                renameSmaliFile(fpath)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Please provide root directory for smali'
        sys.exit(2)
    smali_root = sys.argv[1]
    print 'Begine to process *.smali under ', smali_root
    processSmali(smali_root)
    print 'Done'
{% endcodeblock %}



