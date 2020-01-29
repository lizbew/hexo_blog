---
title: 尝试了下go module，换用更简单的glide
date: 2019-12-31 07:08:12
tags: [go module,  glide]
---

# go module的基本用法

$GOPTAH/pkg/mod/..

go mod edit -require=
go mod edit -replace=

参考：


# go module使用中遇到的问题


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
$ glide create                            # Start a new workspace
$ open glide.yaml                         # and edit away!
$ glide get github.com/Masterminds/cookoo # Get a package and add to glide.yaml
$ glide install                           # Install packages and dependencies
# work, work, work
$ go build                                # Go tools work normally
$ glide up                                # Update to newest versions of the package
```

在已有的项目中运行 `glide init` 全扫描所有go代码文件中的依赖包， 生成glide.yaml文件。 这个命令运行是一个过程式的过程，会下载依赖包的版本信息，然后询问你选择依赖项版本的策略，如选择minor小版本内的或者是限定在patch版本内。

![glide-init](images/post/2019-12-31/glide-init.png)

接下来运行 `glide install` 下载依赖包。在打印的输出看到几行`[ERROR]`， 不能下载包`golang.org/x/sys/unix`。 

![glide-init](images/post/2019-12-31/glide-install-error.png)

这种未知原因的错误需要从 github.com/golang/unix 手动下载包来解决。 如下在`glide.yaml`指定依赖项的repo, 再继续运行 `glide install`，如此替换golang.org 下所有包，直到安装成功。

```yaml
import:
- package: golang.org/x/sys/unix
  repo: https://github.com/golang/sys
  vcs: git
```
