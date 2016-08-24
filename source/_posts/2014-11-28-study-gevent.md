---
layout: post
title: "学习gevent之基本用法"
description: "学习gevent的用法，并实现一个异步查询电话号码归属地"
category: python
tags: [python, gevent, concurrent, urllib2]
---

花了点时间学习gevent, 目前只了解其基本用法，但还不清楚实现原理。

## 一些学习资源：

* gevent site [http://gevent.org/](http://gevent.org/)
* gevent in GitHub [https://github.com/gevent/gevent](https://github.com/gevent/gevent)
* Gevent Tutorial [http://sdiehl.github.io/gevent-tutorial/](http://sdiehl.github.io/gevent-tutorial/)
* Gevent Tutorial 中文翻译 [http://xlambda.com/gevent-tutorial/](http://xlambda.com/gevent-tutorial/)

## 简单用法

下面的代码来自[Gevent Tutorial](http://sdiehl.github.io/gevent-tutorial/). 首先定义两函数`foo()`和`bar()`来实现具体的操作，再由`gevent.spawn()`创建`Greenlet`对象来执行`foo()`/`bar()`，最后`gevent.joinall()`来等待两`greenlet`执行结束。`foo()`/`bar()`中调用`gevent.sleep(0)`来显式切换到不同的`Greenlet`。

{% codeblock lang:python %}
import gevent

def foo():
    print('Running in foo')
    gevent.sleep(0)
    print('Explicit context switch to foo again')

def bar():
    print('Explicit context to bar')
    gevent.sleep(0)
    print('Implicit context switch back to bar')

gevent.joinall([
    gevent.spawn(foo),
    gevent.spawn(bar),
])
{% endcodeblock %}

要点：

* 使用`gevent.spawn()`或[直接创建`Greenlet`](http://gevent.org/intro.html#lightweight-pseudothreads)来新建执行单元
* `join()`函数来等待所有执行单元结束
* 执行的函数里在需要等待时能切换到其它，比如`gevent.sleep(0)`， 或是网络等待事件
* [Monkey patching](http://gevent.org/intro.html#monkey-patching)打补丁来支持gevent, 如：

{% codeblock lang:python %}
>>> from gevent import monkey; monkey.patch_socket()
>>> import urllib2 # it is usable from multiple greenlets now
{% endcodeblock %}

* 提供一些数据结构来支持Greenlet之间的通信，如`gevent.queue.Queue`

## 使用gevent来实现并行查询数据

作为练习，实现的功能是手机号码归属地查询。代码仅为学习交流之用，故隐藏了查询所使用的url, 切勿用于其它目的，且本人不对使用产生的任何后果负责。

* `tasks = Queue()`用于存放phone number, `leadWorker()`生成号码放在`tasks`中，`queryWorker()`从`tasks`中取出一个号码查询
* 查询的结果放入`resultQue = Queue()`， `writeWorker()`会读取该queue的内容然后写入文件
* 1个`leadWorker()`和10个`queryWorker()`同时工作

{% codeblock lang:python %}
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import gevent;
from gevent import monkey;  monkey.patch_socket(); monkey.patch_ssl()
from gevent.queue import Queue, Empty
import urllib2
import json
import random

REQ_URL = 'https://....xxx.com/callback?...&phone={0}&...'

tasks = Queue()
resultQue = Queue()
runningQue = Queue()

completed = False

def queryWorker(n):
    runningQue.put(n)
    try:
        while not tasks.empty() or not completed:
            try:
                phn = tasks.get(timeout = 30)
            except Empty:
                continue
            print n, ' - ', phn
            req = urllib2.Request(REQ_URL.format(phn), headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) Chrome/39.0.2171.71'})
            resp = urllib2.urlopen(req)
            resp_content = resp.read()
            if len(resp_content) > 0:
                i = resp_content.find('(')
                if i > 0:
                    j = resp_content.rfind(')')
                    jsonData = json.loads(resp_content[i+1:j])
                    if jsonData['data']:
                        line = '{0}|{1}|{2}|{3}'.format(phn, jsonData[u'data'][u'operator'].encode('utf-8'), jsonData[u'data'][u'area'].encode('utf-8'), jsonData[u'data'][u'area_operator'].encode('utf-8'))
                        resultQue.put(line)
            gevent.sleep(0.2)
    finally:
        runningQue.get(timeout = 1)
    print n, ' Completed'

def leadWorker():
    global completed
    n = 0
    for i in xrange(10):
        for j in xrange(10000):
            t = ''.join([str(random.randint(0,9)) for _ in range(4)])
            phn = '13%d%04d%s'%(i, j, t)
            tasks.put(phn)
            n += 1
            if n == 100:
                gevent.sleep(30)
            n = 0
    completed = True
    print 'Lead Worker Completed'

def writeWorker():
    global resultQue, runningQue
    fd = open('phn_area.txt', 'w')
    try:
        while not resultQue.empty() or not runningQue.empty():
            try:
                line = resultQue.get(timeout = 1)
            except Empty:
                continue
            fd.write(line)
            fd.write('\n')
    finally:
        fd.close()
    
workers = [gevent.spawn(queryWorker, i) for i in range(10)]
workers.append(gevent.spawn(leadWorker))
workers.append(gevent.spawn(writeWorker))
gevent.joinall(workers)

#fix: gevent.hub.LoopExit: This operation would block forever
#resultQue.put(StopIteration)
#fd = open('phn_area.txt', 'w')
#for line in resultQue:
#    fd.write(line)
#    fd.write('\n')
#fd.close()
print 'All Completed'
{% endcodeblock %}

***

## 后记

尽管添加了try-catch，但在获取1万个号码地区时还是遇到了一些问题。代码运行开始时设定的worker数是10个，但在接近完成一半时发现有些worker不打印log了：第一次结尾时有5个worker打印出完成，第二次时只有一个了。可能是有等待，两次都没有正常退出，只好ctrl+c强制结束了。这是一个问题，需要解决。

后来看到有错误`Connection timed out`。尽管有try-finally，但看样子是没catch住。

<pre>
Traceback (most recent call last):
  File "/usr/local/lib/python2.7/dist-packages/gevent/greenlet.py", line 327, in run
    result = self._run(*self.args, **self.kwargs)
  File "phn.py", line 29, in queryWorker
    resp = urllib2.urlopen(req)
  File "/usr/lib/python2.7/urllib2.py", line 127, in urlopen
    return _opener.open(url, data, timeout)
  File "/usr/lib/python2.7/urllib2.py", line 404, in open
    response = self._open(req, data)
  File "/usr/lib/python2.7/urllib2.py", line 422, in _open
    '_open', req)
  File "/usr/lib/python2.7/urllib2.py", line 382, in _call_chain
    result = func(*args)
  File "/usr/lib/python2.7/urllib2.py", line 1222, in https_open
    return self.do_open(httplib.HTTPSConnection, req)
  File "/usr/lib/python2.7/urllib2.py", line 1184, in do_open
    raise URLError(err)
URLError: <urlopen error [Errno 110] Connection timed out>
<Greenlet at 0x7f98468acc30: queryWorker(6)> failed with URLError
</pre>
