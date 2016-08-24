---
layout: post
title: "基于GAE实现简单的功能"
description: ""
category: web
tags: [GAE]
---

原始发布网址: http://blog.viifly.com/blog/posts/3001

最总几周的晚上都在弄的GAE, 想整点东西出来。不过没什么好想法，只能先从blog开始了。 Blog的后台数据结构是比较简单的，一个存blog 内容的主表，再加上category, tag之类子表。后台的代码是比较容易实现的，当开始写UI部分时就头大了，UI的好坏不单单是技术问题了。不会photoshop,也没有对UI有过分析，当直接从HTML开始时，就只能拼凑代码，然后打开浏览器再看看效果了。基本都是找sample, 再copy+paste。一套现成的UI库就显示极其重要了。

再说说从GAE提供的service出发想到的一个功能。 blog除了从datastore里拿content生成内容外，总会有那么个静态页面的， 比如about。 自己在开发blog程序时也添加了page页面，分为两种：一种是有layout的，从datastore里或是文件读取内容，再填充到layout template里，另一种是不用layout的，内容就是整个HTML，可以直接返回到客户端的。在我的blog里page功能是整个HTML功能存到datastore里。GAE提供了Blobstore service，就是用来存上传的二进制文件，还有相应的接口来返回文件到客户端。page中引用到的css/img/css就可以存放到Blobstore 。Page+BlobStore， 太完美了。

当我在编辑一个page 的HTML时，想到了google site，突然间觉得它们太类似了。我编辑HTML是在textarea里，而如果改成全功能的可视化编辑器的话，那离google site就不远了。^-^， 开始YY了。

其实实现这个page功能，只是想展示下学习到的HTML5。不过还没开始HTML5学习，这是下一步打算。HTML5的展示可以只需要静态HMLT，再加上js+css+img；会先做一个gallery页面，再添加到其它page的link。 在学习D3库时，在sample gallery中也有类似的设计，不过页面存放在github gist上。 D3的通过gist的API得到一个文件列表，每一个sample都是从一个index.html开始。有gist的这样的免费资源，建个草根站点就比以前容易多。一个站点就可以全部依靠免费建立起来：最基本的代码可以放在GAE或新浪、百度等的App Engine，jquery等js引用公共CDN， 代码放github，等等。从另一个角度讲，提供单一功能的service API，只要足够好，也是是市场的。

