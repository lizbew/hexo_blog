---
layout: post
title: "web页面图形延迟加载"
description: ""
category: web
tags: [jQuery, js, img]
---

原始发布于： http://blog.viifly.com/blog/posts/5852562955698176

查看backbone js的doc页面时，偶然看到源代码里用到库jquery.lazyload.js，于是研究了下。 浏览了下源代码，再查看文档[lazyload](http://www.appelsiini.net/projects/lazyload)。

##使用lazyload##

    <img class="lazy" src="img/grey.gif" data-original="img/example.jpg" width="640" height="480">
    {: class='prettyprint lang-html' }

<!-- language: html -->

    <script src="jquery.js" type="text/javascript"></script>
    <script src="jquery.lazyload.js" type="text/javascript"></script>

<!-- language: js -->
    $("img.lazy").lazyload();

##原理##

需将img的src设置一个占位图片,而真正的图片放在参数data-original。将每一个需要延时加载的`<img/>`绑定scroll事件；当scroll时判断图片的位置，当需要显示时在js里将src替换成data-original的值。


另有[preloading img](http://www.appelsiini.net/2007/6/sequentially-preloading-images)

