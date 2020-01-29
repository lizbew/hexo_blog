---
title: 关于nodejs与golang中的bcrypt
date: 2020-01-25 20:12:38
tags: [bcrypt, bcryptjs]
---

这两天在改写一个简单的bookmark工程， 从nodejs改为golang, nodejs中数据库保存的密码字段用了`bcryptjs`来加密， golang中来使用bcrypt加密算法也相应研究了下。

## bcrypt

bcrypt 算法主要是来对密码进行hash再保存的。bcrypt对数据计算hash之前， 会先生成一串salt, 这串salt会保存在最终生成的hash串里； 当需要验证密码时也需要这串salt。 然后具体的加密算法是`blowfish`。

## 在nodejs中使用bcryptjs

参考 https://github.com/dcodeIO/bcrypt.js

使用之前需要在项目中先安装包

```bash
npm install bcryptjs --save
```

```js
var bcrypt = require('bcryptjs');

var salt = bcrypt.genSaltSync(10);
var hash = bcrypt.hashSync("Password-001", salt);
console.log('hash=' + hash);

var valid = bcrypt.compareSync('Password-001', hash);
console.log('compare-1: ' + valid);

valid = bcrypt.compareSync('Password-002', hash);
console.log('compare-2: ' + valid);
```

运行结果：

```
> node index.js

hash=$2a$10$AFqmH2Y3tgNvUeEOV4H3UuSZzH8nlfNAXEJTukpbpArakftGizlDm
compare-1: true
compare-2: false
```

示例里使用的是都是同步方法，方法名带Sync。bcrypt也同时支持异步方法，方法名不带Sync。`bcrypt.genSaltSync()`的参数为计算次数， 值为4到31； 值越大，计算hash值所需的时间就越长，相应的被攻破所需的时间也越长。


简单读了下[bcryptjs的源码](https://github.com/dcodeIO/bcrypt.js)，得到hash串总长度是60, 前一段是salt，后面大概31位(未实际查询算法文档)字符是真正的hash值。 salt部分`$2a$10$`是用`$`分隔的字段， 2a是版本号， 10是加密次数;  这个前缀之后是生成的16字节的随机数， 再base64编码。

## 在golang 中使用bcrypt

参考 https://godoc.org/golang.org/x/crypto/bcrypt

在golang 的官方包也是提供了bcrypt. 但从[blowfish的文档](https://godoc.org/golang.org/x/crypto/blowfish)中看，并不推荐使用blowfish算法. 

```go
package main
import "golang.org/x/crypto/bcrypt"

ash, err := bcrypt.GenerateFromPassword([]byte("soem-pass"), 4)
err := bcrypt.CompareHashAndPassword(ash, []byte("soem-pass"))
```
