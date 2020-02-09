---
title: 尝试了下go module，换用更简单的glide
date: 2019-12-31 07:08:12
tags: [go module,  glide, golang]
---

# go module的基本用法

go mod 模块管理是在go 1.11之后推出的包管理工具。 开启之后， 项目代码可以放在任意目录而不是必须在$GOPATH之下； 下载的包会放置在目录`$GOPTAH/pkg/mod/`, 同时忽略 $GOPATH 和 vendor 文件夹.

包的名称定义和依赖包保存在文件go.mod中， 安装之后的go.sum保存实际使用的版本信息。依赖的包中有go.mod文件的话，也会下载其依赖的包。

```bash
go mod init project ## 初始化项目
go mod edit -require=github.com/gin-gonic/gin@v1.5.0  ## 添加依赖包及其版本， 版本是必须的
go mod edit -replace=golang.org/x/sys=github.com/golang/sys@v0.0.0 # 替换包
go mod edit -exclude=cloud.google.com/go@v0.0.0 #排除
go mod tidy # 整理依赖包，可能会删除未使用的
go mode tree
go mod graph
```
    
参考： 

https://colobu.com/2018/08/27/learn-go-module/

# go module使用中遇到的问题

遇到最大的问题是`golang.org/x/..` 这类的包不能直接下载，遇到网络问题停止下来时用`go mod edit -repace=..`来添加替换。依赖的包没有tag， 使用的是git hash串， 然后同一个包就会出现各种不同git hash, 得不停的加replace。 实在忍受不了，只能放弃。

# glide的基本用法

glide是基于go vendor的方案，将依赖的包下载在项目的vendor目录下。glide的依赖配置文件为glide.yaml, 下载依赖项之后将使用的版本信息保存在文件 glide.lock。 尝试过之后，感觉和npm 的包管理在非常的类似。 

项目地址 https://github.com/Masterminds/glide

## 安装

最简单的安装方法:

```bash
curl https://glide.sh/get | sh
```

在macos 下可以使用Homebrew来安装最新版本:

```bash
brew install glide
```
## 基本用法

```bash
## create new project folder and cd to it fistly
$ glide create                            # Start a new workspace
$ open glide.yaml                         # and edit away!
$ glide get github.com/Masterminds/cookoo # Get a package and add to glide.yaml
$ glide install                           # Install packages and dependencies
# work, work, work
$ go build                                # Go tools work normally
$ glide up                                # Update to newest versions of the package
```

在已有的项目中运行 `glide init` 全扫描所有go代码文件中的依赖包， 生成glide.yaml文件。 这个命令运行是一个过程式的过程，会下载依赖包的版本信息，然后询问你选择依赖项版本的策略，如选择minor小版本内的或者是限定在patch版本内。

![glide-init](/images/post/2019-12-31/glide-init.png)

接下来运行 `glide install` 下载依赖包。在打印的输出看到几行`[ERROR]`， 不能下载包`golang.org/x/sys/unix`。 

![glide-init](/images/post/2019-12-31/glide-install-error.png)

这种未知原因的错误需要从 github.com/golang/unix 手动下载包来解决。 如下在`glide.yaml`指定依赖项的repo, 再继续运行 `glide install`，如此替换golang.org 下所有包，直到安装成功。

```yaml
import:
- package: golang.org/x/sys/unix
  repo: https://github.com/golang/sys
  vcs: git
```
