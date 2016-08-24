---
layout: post
title: "使用Echarts可视化数据"
description: "analyze data from one location based application, show chart with ECharts"
category: web
tags: [data-analyze, echarts]
---

时间过得真快， 一个多月都没有写blog了。

上周末用百度开源的图形库画了几个图。 数据来源是一款基于地理位置的手机应用， 按照网上的方法修改了android APK， 将返回的HTTP数据保存为一个个文件再导出来进行分析。 使用的数据是附近的人, 1KM范围内的， 数量量太小， 可能也不能作为参考， 只是看看效果。

## 先看图

* 附近的人中男女比例 - 男数量比女数量的双倍还多

![chart-1](/images/post/2015-06-15/chart-1.png)

* 年齡分布 - 年轻人的世界， 主要是20 ～ 30

![chart-2](/images/post/2015-06-15/chart-2.png)

* VIP 比例 - 男女都有约5%左右的VIP用户， 其中女比例比男略多

![chart-3](/images/post/2015-06-15/chart-3.png)

* 使用手机类型 - IOS和android各占一半

![chart-4](/images/post/2015-06-15/chart-4.png)

## 使用工具

* WebStorm 生成的html5-boilerplate项目
* 从百度CDN加载了jquery, underscore 和 bootstrap
* 数据可视化图使用百度开源的 [ECharts](http://echarts.baidu.com/)
* 我的代码为[nearby-chart](https://github.com/lizbew/nearby-chart), 看看src/js/main.js就行了

