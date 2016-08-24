---
layout: post
title: "something about wsgi"
description: ""
category: python
tags: [python, wsgi, webpy]
---

这两天读了下python标准库wsgiref的代码，对wsgi加深了了解。尽管我的原本意图是读web.py的源码，但这是接下来一步了。

现看下wsgi application的写法，下面摘自[SAE 文档](http://sae.sina.com.cn/doc/python/tutorial.html#hello-world)。贴python manuals 的code可能更好，不过都差不多。


{% codeblock lang:python %}
import sae

def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello, world!']

application = sae.create_wsgi_app(app)
{% endcodeblock %}
wsgi application主要是实现上面的app方法，function或object都行，只要是callable。app接受两个参数，environ是dict类型的环境变量，包含请求路径/方法/参数等；而start_response是回调函数，传递响应状态和响应头。app还需要返回iterable的响应内容。

wsgi的server端会调用这个app方法。在调用前会根据request来设置environ的值，当app()返回后将响应状态/头/内容发送到客户端。

标准库wsgiref使用SimpleHTTPServer来实现. 于是也读了SocketServer, BaseHTTPServer和CGIHTTPServer。WSGI和CGI是很类似的，都使用了环境变量来传递接受到的request, 只不过CGI是运行外部程序来返回结果，而WSGI是调用python方法。

