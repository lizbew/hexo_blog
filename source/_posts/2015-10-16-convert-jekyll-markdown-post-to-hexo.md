---
layout: post
title: "Convert Jekyll markdown post to Hexo"
description: ""
category: python
tags: [markdown, hexo, jekyll]
---

这两天配置了Hexo来生成博客，其文档中的迁移部分指示说将jekyll的@\_post@路径下的文件直接复制到hexo的目录下即可。但由于jekyll post 有些使用了自定义的插件，在hexo generate时会抛了异常，于是写了个脚本来完成插件标签的处理。

代码共享在 https://github.com/lizbew/code-practice/blob/master/convert_md_post.py

主要完成下面三个功能:

* 删除 \{\% include JB/setup \%\}这种标签行
* 将\{\% highlight python \%\} 代码块标签转成\{\% codeblock lang:python \%\}
* 一些post 中还留有markdown python 库中的使用的代码块， 如带4个空格缩进加:::lang的代码块，也会转换成使用\{\% codeblock \%\}

