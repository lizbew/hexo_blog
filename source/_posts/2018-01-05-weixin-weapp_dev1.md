---
title: 最近在研究小程序
date: 2018-01-05 20:25:51
tags: weapp
---

# 最近在研究小程序， 对照着wafer-node-sdk用java实现一个简单的session server。只能运行起来测试， 并不能实现使用。

小程序客户端使用 https://github.com/tencentyun/lab-rps-client/

* 使用Vert.x框架实现， 使用的全是异步回调， 考虑改成用RxJava的
* 数据库为hsqldb, 并不能持久化保存数据
* 还没实现socket相关的功能
* Vert.x程序会打包成一个fatJar， 直接运行。 话说打包之后有15M, 连接虚拟机上传速度超极之慢，出一点Exception之后改改再上传费时间。 不过可以考虑使用ssh远程端口转发

代码共享在github之上， 以后再花时间改：　https://github.com/lizbew/wafer-java-session　。


下面是关于小程序的一些参考资料：

* 小程序官方文档 https://mp.weixin.qq.com/debug/wxadoc/dev/
* wafer https://github.com/tencentyun/wafer
* 小程序实验室 https://cloud.tencent.com/developer/labs/lab/10004
* wepy https://tencent.github.io/wepy/
* awesome-wepy https://github.com/aben1188/awesome-wepy
* zanui-weap https://github.com/youzan/zanui-weapp
* minui https://github.com/meili/minui
* wepy-wechat-demo https://github.com/wepyjs/wepy-wechat-demo

之后还要了解一些关于小程序自动化测试。

----

远程端口转发

```bash
ssh -R 8080:127.0.0.1:8080 root@remote_ip
````
