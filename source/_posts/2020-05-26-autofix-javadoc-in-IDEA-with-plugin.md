---
title: 使用IDEA插件自动补全javadoc
date: 2020-05-26 23:41:13
tags: ['javadoc', 'idea', 'plugin', 'java']
---

工作有代码整改要求， 要给所有java代码添加copyright文件头，类和方法补全javadoc注释。copyright 与javadoc使用了不同的方案来修复： 

1. copyright 使用shell脚本来实现，查找文件夹下所有的java文件，将copyright 与文件内容copy到一个新的临时文件里， 再删掉文件， 将临时文件重命令为原文件。 这个方案对同一个文件只能操作一次， 否则会出现多次插入copyright的情况；可以借助git, 修改完之后review改动检查java文件都只插入一次。
2. 类与方法添加javadoc, 需要借助IDE的插件来实现。 在网上搜索一番之后， 发现Eclipse中可以使用[JAutodoc](http://jautodoc.sourceforge.net/)， 而IDEA中的插件[javadoc](https://plugins.jetbrains.com/plugin/7157-javadoc)。本人使用IDEA开发, 只尝试了相应的插件，效果还不错。[javaDoc github](http://setial.github.com/intellij-javadocs)


## 批量插入copyright

脚本来自于 https://blog.csdn.net/tiplip/article/details/13296951

* copyright.txt 保存版权信息，根据需要进行修改
* insert_license.sh, 插入copyright的脚本， windows下在git bash里执行

```bash
#!/bin/bash
win_path='D:\src\java'
search_path=/$(echo $win_path | sed 's/\\/\//g' | sed 's/://g')

shopt -s globstar nullglob extglob
for i in ${search_path}/**/*.@(java);do
  if ! grep -q Copyright $i
  then
    cat copyright.txt $i >$i.new && mv $i.new $i
  fi
done
```


## idea javaDoc 插件配置

javaDoc插件里的注释风格可以根据需要修改。配置路径 settings - Tools/javaDoc 选择template页，针对类注释class level、方法level注释有不同的模板。 比如对class level级别的注释需要添加`@since yyyy-MM-dd`, 在class/interface/enum/+等4条目里都需要加上。

如上只是针对存量的java代码补回， 而对新建java文件， 可以使用IDEA中的CopyrightProfile/File Template/Live Template等配置来实现。

