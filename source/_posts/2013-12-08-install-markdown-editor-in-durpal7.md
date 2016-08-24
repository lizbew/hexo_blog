---
layout: post
title: "Durpal 7下安装Markdown编辑器"
description: ""
category: web
tags: [durpal, php, markdown]
---

原始发布于： http://blog.viifly.com/blog/posts/5818443735498752

上周在免费空间上安装了Drupal 7，前两天安装markdown编辑插件。


## 插件

Markdown和code highter安装在*sites/all/modules*目录下。从drupal.org下载插件包后下解压到该目录就OK了，在admin中moduels页面就出现新添加的插件。

 - [Markdown filter](https://drupal.org/project/markdown)
 - [Markdown editor for BUEditor](https://drupal.org/project/markdowneditor)
 - [BUEditor](https://drupal.org/project/bueditor)
 - [SyntaxHighlighter](https://drupal.org/project/syntaxhighlighter)

SyntaxHighlighter是基于js的语法高亮，依赖的js包需要另外下载安装。下载[SyntaxHighlighter](http://alexgorbatchev.com/SyntaxHighlighter/download/)压缩包后，解压于目录*sites/all/libraries*。

## 配置

以admin身份登陆后，在modules页面可以看到所有安装的module。所有新添加的module都要勾选来enable.
![Enable Modules][1]{. style="width:650px;"}

要editor支持markdown,还需要添加markdown format.
![Add Markdown Format][2]{. style="width:650px;"}

markdown filter中filter处理顺序是很重要的，Syntax Highligher的要先于markdown，否则会有代码不能高亮而出现混乱的问题。
![Filter Process Order][3]

## 语法高亮

SyntaxHighlighter插件已经安装了，在插入代码时需要`<pre class="brush: lang">...</pre>`来包围代码。

最后看下[实际效果][4].
![Syntax Hightlight][5]

  [1]: /images/post/drupal_config_modueles.png
  [2]: /images/post/drupal_add_format.png
  [3]: /images/post/drupal_md_filter_order.png
  [4]: http://snippetis.com/s/node/3
  [5]: /images/post/drupal_syntax_hl.png

