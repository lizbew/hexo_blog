---
layout: post
title: "安装Ghost"
description: ""
category: web
tags: [Ghost, nodejs, forever]
---

原始发布于： http://blog.viifly.com/blog/posts/5779342353235968

此Ghost并非大家所熟悉的安装操作系统的那款，而是基于Node.js的博客系统，官网为[ghost.org][1]。今天花了点时间来安装到一个运行ArchLinux的ARM盒子。要运行Ghost, 当然需要先安装node.js和npm，由于之前已经安装好了，就跳过此步。

## 安装Ghost

从Ghost页面[下载][2]最新的源码包，当前版本还是0.3。解压并进入到ghost,更改*config.js*后可以开始体验了。

{% codeblock lang:bash %}
wget https://ghost.org/zip/ghost-0.3.3.zip
unzip -uo ghost-0.3.3.zip -d ghost
cd ghost
npm install --production
npm start
{% endcodeblock %}

*config.js*中需要更改地方是url, host与port。url我改为真实的IP地址，host改为`'0.0.0.0'`这样从其它机器就可以访问了，而port端口保存不变。访问http://localhost:2368/就可以查看页面结果；而访问http://localhost:2368/ghost是管理页面，第一次访问会注册新的账号。

{% codeblock lang:js %}
production: {
    url: 'http://my-ghost-blog.com',
    mail: {},
    database: {
        client: 'sqlite3',
        connection: {
            filename: path.join(__dirname, '/content/data/ghost.db')
        },
        debug: false
    },
    server: {
        // Host to be passed to node's `net.Server#listen()`
        host: '127.0.0.1',
        // Port to be passed to node's `net.Server#listen()`, for iisnode set this to `process.env.PORT`
        port: '2368'
    }
},
{% endcodeblock %}


## 后台运行Ghost

以`npm start`运行Ghost所有log都输出在console，且不能关闭。Ghost的install guide上给出了一些deploy方案，而这次选用的是Forever ([https://npmjs.org/package/forever][3])。

{% codeblock lang:bash %}
npm install forever -g  #以root用户安装forever
NODE_ENV=production forever start index.js  #启动Ghost
forever stop index.js  # 停止Ghost
forever list  # 查看运行状态
{% endcodeblock %}

之前阅读了简书的一篇文章: [在NITROUS.IO免费架设GHOST并绑定你自己的域名][4]

  [1]: http://ghost.org/
  [2]: https://ghost.org/download/
  [3]: https://npmjs.org/package/forever
  [4]: http://jianshu.io/p/MFSrCq

