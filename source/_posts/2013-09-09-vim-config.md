---
layout: post
title: "vim的配置"
description: ""
category: tool
tags: [vim, vimrc, vundle]
---

原始发布于： http://blog.viifly.com/blog/posts/5681726336532480

今天主要收获就是学习VIM的配置了。首先是vimrc中常用的一类命令了，[参考][1]。然后学习易水博客的中系列文章[vi/vim使用进阶][2]。下面简单地写下摘要。

##vimrc相关命令##

 - vimrc 文件路径。vim安装进带的示例为`$VIMRUNTIME/vimrc_example.vim`，使用为`~/.vimrc`。而windows下默认使用`$VIM\_vimrc`， 也是位于安装目录下的；不过也可以新建使用`%USERROFILE%\_vimrc`。
 - session文件，保存VIM的相关配置。`:mksession [file]`命令来创建一个会话文件，默认文件名为Session.vim。session文件保存的内容由‘sessionoptions’选项确定，缺省为“blank,buffers,curdir,folds,help,options,tabpages,winsize”。:set sessionoptions-=curdir， :set sessionoptions+=sesdir。加载session：`:source session-file`
 - viminfo，操作历史记录。用:wviminfo [file]来创建viminfo文件，用:rviminfo [file]来读取
 - [保存项目相关配置][3]

##Vundle管理插件##

[Vundle][4]是VIM的插件管理工具(Vim bundle)。由于工作环境主要是windows, 于是尝试在winodws下安装，参考[Vundle-for-Windows][5]。 不过是不能完全按照Vundle wiki来做的： 如下vundle被clone到vimfiles下，而当重开gvim后:BundleInstall时，从github clone的插件却放在.vim下。


<pre class="prettyprint linenums">
cd %USERPROFILE%
git clone https://github.com/gmarik/vundle.git vimfiles/bundle/vundle
gvim _vimrc
</pre>

另外，[Quick Start][6]是在Linux下操作的，需要修改才能用于windows。我将`set rtp+=~/.vim/bundle/vundle/`改为`set rtp+=$userprofile/vimfiles/bundle/vundle/`，所要编辑的文件也是%USERPROFILE%\_vimrc。


  [1]: http://edyfox.codecarver.org/html/_vimrc_for_beginners.html
  [2]: http://easwy.com/blog/archives/advanced-vim-skills-catalog/
  [3]: http://easwy.com/blog/archives/advanced-vim-skills-save-project-configuration/
  [4]: https://github.com/gmarik/vundle
  [5]: https://github.com/gmarik/vundle/wiki/Vundle-for-Windows
  [6]: https://github.com/gmarik/vundle/blob/master/README.md#quick-start
