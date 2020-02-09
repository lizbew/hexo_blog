---
title: create ppstats with vanilla
date: 2018-03-05 23:18:16
tags: [openresty, lua, vanilla]
---

最近看了openresty/lua相关的一点点知识， 然后想折腾个啥，做博客post的访问记录。 关于web框架，研究了下vanilla, 文档不够，功能也不够完善， 真正使用起来还是有一些事情要做的， 完成了这个就不想折腾它了。

## 页面访问逻辑

当用户每打开一个page时， 产生一条访问记录， 同时返回访问总数，更新页面上的访问数量。 在服务器端的大概处理流程如下：

1. 从请求参数中获取appid, host, url， 查询数据库检查appid, host是否合法。非法则不产生记录
2. 访问记录表中添加一条记录
3. redis的中页面url对应的counter加1
4. 返回counter数

设计的数据库表有三个：

1. `reg_application` 记录appid, 及其name。 添加访问记录时需要传递Appid
2. `allow_hosts` appid相关联的host， 只允许记录存的host的访问
3. `visit_log` 单次访问的记录

![数据库表](/images/post/2019-12-08/ppstats-charts-tables.png)

## 代码实现

https://github.com/lizbew/ppstats

![访问流程](/images/post/2019-12-08/ppstats-charts-flow.png)

## Vinalla相关

### 新建工程

vinallia的github 工程文档中是使用源代码中的shell来创建工程和启动程序的, 网上一些文章里是使用luarocks来安装的。我的这个工程是按照luarocks的方式来的， 不过推荐使用源码来安装， 因为luarocks中不是最新的版本，且vanilla缺乏文档，需要查看源代码。

* 安装lua5.1 及luajit, 从apt安装的
* 安装luarocks： sudo apt-get install  luarocks
* 安装vanilla: luarocks install vanilla
* 新建vanilla 工程： vanilla new ppstats
* 启动：  cd ppstats && vanilla start --trace

参考：

* https://github.com/idevz/vanilla
* https://github.com/idevz/vanilla-zh
* http://www.stuq.org/news/557

### 连接redis及postgresql

后台对接数据库服务这块， 开源出的vanilla基本没有相关的功能，需要自己研究。 其中的cache功能，只能作为通用的缓存， 对key的set/get，没有暴露实现counter的功能。

* redis的代码， 参考《Openresty最佳实践》  https://moonbingbing.gitbooks.io/openresty-best-practices/content/redis/auth_connect.html
* postgresql的连接库使用pgmoon: `luarocks install pgmoon` https://github.com/leafo/pgmoon
* 同时使用了openresty官网代码  https://github.com/openresty/openresty.org/tree/master/v2/lua/openresty_org

### vanilla 获取请求头及请求参数 

获取请求参数在文档里是没有的，且不同的版本还有区别。 在早一些的版本中要使用`self:getRequest().headers`, 而在最新的版本中，提供了新的API: `self:getRequest().getHeaders()`

```lua
function JstatsController:index()
    local headers = self:getRequest().headers
    local params = self:getRequest().params

end
```

controller中的`getRequest()`方法来自于vanilla代码中的[controller.lua](https://github.com/idevz/vanilla/blob/master/vanilla/v/controller.lua), 代码运行时会将其通过setmetatable设置成自业务自定义controller的__index， 即继承功能。 

### 遇到的一个坑

vanilla 启动时需要运行nginx, 且要求从PATH路径中可以找到`nginx`， 但我的机器上先安装官方的nginx包， 然后再从源代码安装 的openresty。 PATH路径及linux service中运行的是原生nginx, 所以运行`vanilla start`一直提示nginx.conf 中lua相关的指令无效。 尝试了各种在命令行中定义环境变量都没有成功，也没有找到指定的nginx路径的参数，最后只有修改luarocks中包的代码了。

   $ sudo vim /usr/local/lib/luarocks/rocks/vanilla/0.1.0.rc4-1/bin/vanilla
   需要在.lua文件中定义  VANILLA_NGX_PATH = '/usr/local/openresty/nginx'


###  20190526更新

周末，终于实现了一个简单的js来发送统计消息， 代码位于[ppstats/js](https://github.com/lizbew/ppstats/tree/master/js) 目录下。 使用了webpack来打包js .

* webpack https://webpack.js.org/guides
* babel支持aysnc/await语法的插件 https://babeljs.io/docs/en/babel-plugin-transform-runtime
* fetch https://developer.mozilla.org/zh-CN/docs/Web/API/Fetch_API/Using_Fetch
* isomorphic-fetch https://www.npmjs.com/package/isomorphic-fetch
* query-string https://www.npmjs.com/package/query-string

```
<script src="./ppstats.js"></script>
<script>
    ppstats('http://localhost:9901/', 'appid', function(resp){
        console.log(resp);
    });
</script>
```
