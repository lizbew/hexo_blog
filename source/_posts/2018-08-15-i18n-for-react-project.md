---
title: i18n for react project
date: 2018-08-15 22:03:02
tags: [i18n, react, i18n-pick]
---

参与开发的一个项目最近需要支持多语言， 于是研究了下国际化相关的。项目采用前后端分离开发的单页应用，前端使用react, 开发框架是dvajs 与antd，后台就是常用的spring mvc + mybatis + mysql。 菜单列表是可以在页面配置，存储于数据库，多语言支持就前后端都需要处理了。

在项目的技术方案确定之后，自已也写一个简单的演示程序， 相关的链接也放在github 仓库的readme中， 这里就偷懒不加了。 地址： https://github.com/lizbew/dva-favlist。

## 前端React项目

Antd界面库文档有关于国际化的说明， 所以开始从 Antd LocalProvider入手， 文档中推荐的文档有react-intl 和 react-intl-universa。 考虑到项目文件中还有jquery实现统一主菜单，也有国际化需求，最后选择了 i18next。

* Antd LocalProvider 解决Antd组件内部的多语言支持
* i18next 用于处理项目其它文本的多语言翻译

react组件中文本提取流程， 这里使用了i18n-pick（还可以选择 gm-i18n-migrate）:

* 运行i18n-pick scan 将项目中文文本提取出来
* 在i18n-messages下的json文件中定义语言的key
* i18n-pick export导出key -> message的json文件
* 定义好使用i18n key的相关方法, 如 `intl.get()`
* i18n-pick pick替换react组件中的文本为多语言翻译函数调用 `intl.get("key")`


## 后端java项目

后端多语言主要就是菜单名字翻译， 于是多添加了两张表， 一个为支持的语言列表， 另一个为 key-language-value 定义key对应的多语言文本。 在需要多语言的api接口中，根据cookie值判断当前语言， 再从数据库查询相应的key进行替换。

## 其它

* 语言编码的选择： 使用语言代码-区域代码的格式，如`zh-CN`, `en-US`， 与浏览器 `window.navigator.language`返回结果一致
* 前端js判断当前使用的语言， 优先顺序： 路径参数， cookie值，浏览器当前语言
* 切换语言采用了后端跳转的方式， 当用户选择语言时js触发跳转到一个后台地址， 路径参数带上语言和当前路径，后台代码设置语言cookie之后重定向到上一个页面地址， 整个页面会刷新一次。

