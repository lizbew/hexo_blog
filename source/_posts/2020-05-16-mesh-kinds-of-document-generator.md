---
title: 整理reactjs相关项目文档在内网访问
date: 2020-05-16 08:51:40
tags: [markdown, doc-generate, vuepress, react]
---

最近有个想法，把reactjs技术栈相关的文档收集一下放在内网里，方便小伙伴们一站式学习各种文档。 思路也很简单，找到开源的各种文档生成html, 放在nginx下的子目录里， 再建一个index.html添加到各个子目录的链接。

遇到问题：
1. 一是开源文档一般都是markdown， 自己下载源文件编译成html， 这个容易解决， 只是安装编译要花点时间精力
2. 二是网上开源项目文档站点主要是以子域名的方式来访问， 文档路径都是在根目录/开始的。移内网编译时需要修改为从子目录访问， 不然就会出现资源引用不到，或者链接无法跳转等。
3. 三是文档中引用的外网资源如比图片等，尽量改成本地引用，要将图片下载到静态目录里。

于是就开始了对不同项目中使用的Markdown文档的一番了解。 本地构建测试环节， 计划是编译完各项目的文档之后， 都移到dev-docs下子目录里， 再使用`serve`命令启动静态文件服务器来预览效果。 目前要构建的项目有如下几个。

* react-js https://zh-hans.reactjs.org/
* redux-in-chinese http://cn.redux.js.org/ 
* react-router-cn https://github.com/react-guide/react-router-cn
* dvajs https://github.com/dvajs/dva
* umijs https://github.com/umijs/umi
* ant design v3 https://3x.ant.design/
* webpack
* es6 http://es6.ruanyifeng.com/

## React

git https://github.com/reactjs/zh-hans.reactjs.org

React文档使用 [gatsby](https://www.gatsbyjs.org/docs/)搭建， 需要node 12的环境， 在macos上使用了nvm 来管理不同node， 所以只需要`nvm install 12 && nvm use 12`就可以切换了。 

build的命令为`npm run build`, 在package.json对应的脚本为`gatsby build  --prefix-paths`, build生成的文件位于public。使用子目录来访问，在配置文件gatsby-config.js中添加项`pathPrefix`. 参考文档 https://www.gatsbyjs.org/docs/recipes/deploying-your-site#preparing-for-deployment

在build过程中遇到访问连接的问题`Error: connect ECONNREFUSED 0.0.0.0:443`, 是由于某magic的问题，对github某一个域名解析返回了'0.0.0.0'这个ip。解决办法是将plugins/gatsby-source-react-error-codes插件中对外网的访问， 改为从文件中读取内容。

## redux/react-router

redux-in-chinese git https://github.com/camsong/redux-in-chinese

这两个使用[gitbook](https://github.com/GitbookIO/gitbook)来生成文档。 但我本地构建时遇到`Error: Cannot find module 'internal/util/types'`， 即使是使用nvm 切换到node 8还是同样错误。gitbook-cli已经不再维护， 暂放弃。

## dvajs

文档使用vuepress, 构建命令在项目的子目录 website中运行 `npm install`。 vuepress的配置文件为docs/.vuepress/config.js, 添加项`base: '/xx/'`来生成子目录访问的， 这个路径一定要带上最后一个斜杠。 参考 https://vuepress.vuejs.org/zh/config/#base

## ant design v3 

ant design的构建工具为[bisheng](https://github.com/benjycui/bisheng), 其实觉得这个工具被使用的少。build命令为`npm run site`， 配置文件`site/bisheng.config.js`中添加项`root:'/xx/`来构建子目录访问的文档。

## umijs

umijs本身是一个web框架，它的文档就是自身工具来build的。使用了node12，项目源码中带有yarn.lock,  所以使用yarn install先安装依赖，再 `yarn run build && yarn run docs:build`来生成文档。在配置文件`.umirc.ts`添加`base`与`publicPath`两个项指向相同的子目录。 

