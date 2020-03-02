---
title: gin 源码阅读
date: 2020-02-09 20:32:32
tags: [gin, golang]
---

[gin](https://github.com/gin-gonic/gin) 是golang流行的web framework，API简单易用，很适用用来做HTTP API开发。 

## 基础结构体

先看下gin最简单的例子，来自于gin的github。先创建一个应用对象，再绑定`GET /ping`请求处理函数， 最后run.

```golang
package main

import "github.com/gin-gonic/gin"

func main() {
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})
	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}
```

这里上涉及两个比较重要的结构体:

1. [`type Engine struct`](https://github.com/gin-gonic/gin/blob/master/gin.go#L55) 由gin.Default() 返回的结构体，整个应用的核心
2. [`type RouterGroup struct`](https://github.com/gin-gonic/gin/blob/master/routergroup.go#L41) 处理请求URL匹配，还有配置请求URL. `r.GET("/ping", func(c *gin.Context) {})` 即是有使用到这个结构体的方法
3. [`type Context struct`](https://github.com/gin-gonic/gin/blob/master/context.go#L43) 请求处理函数的上下相关的信息，获取请求参数，发送响应内容等。

## 模型绑定与校验

gin中的绑定函数分为两类:

1. Must bind, 必须绑定，失败就直接返回给客户端。 `Bind`, `BindJSON`, `BindXML`, `BindQuery`, `BindYAML`, `BindHeader`
2. Should bind, 这类绑定失败返回一个error而不是直接返回， 这样就可以在代码里进行判断并做相应的处理。`ShouldBind`, `ShouldBindJSON`, `ShouldBindXML`, `ShouldBindQuery`, `ShouldBindQuery`, `ShouldBindHeader`

``` golang
// Binding from JSON
type Login struct {
	User     string `form:"user" json:"user" xml:"user"  binding:"required"`
	Password string `form:"password" json:"password" xml:"password" binding:"required"`
}

	// Example for binding JSON ({"user": "manu", "password": "123"})
	router.POST("/loginJSON", func(c *gin.Context) {
		var json Login
		if err := c.ShouldBindJSON(&json); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
        }
        ...
    }
```

结构体`Login`的字段Tag都包含了`binding:"required"`, 用来指定字段必须的校验。 那`binding`是在哪里处理的呢？ 查看代码  https://github.com/gin-gonic/gin/blob/master/binding/default_validator.go, `lazyinit()`中有一段`v.validate.SetTagName("binding")`。 gin的readme 有说明使用了[go-playground/validator/v10](https://github.com/go-playground/validator) 来做校验， 这段代码就是来指定校验规则使用标签`binding`来配置了。

``` golang
func (v *defaultValidator) lazyinit() {
	v.once.Do(func() {
		v.validate = validator.New()
		v.validate.SetTagName("binding")
	})
}
```

还有另外一个问题： 这个validator的校验规则是在什么时候被调用到的呢？肯定是调用`c.ShouldBindJSON(&json)` 这类函数里的时候了。 最后是进入`validate`里了。

```golang
// file: gin/context.go
// ShouldBindJSON is a shortcut for c.ShouldBindWith(obj, binding.JSON).
func (c *Context) ShouldBindJSON(obj interface{}) error {
	return c.ShouldBindWith(obj, binding.JSON)
}

// ShouldBindWith binds the passed struct pointer using the specified binding engine.
// See the binding package.
func (c *Context) ShouldBindWith(obj interface{}, b binding.Binding) error {
	return b.Bind(c.Request, obj)
}

// file: gin/binding/json.go
func (jsonBinding) Bind(req *http.Request, obj interface{}) error {
	if req == nil || req.Body == nil {
		return fmt.Errorf("invalid request")
	}
	return decodeJSON(req.Body, obj)
}

func decodeJSON(r io.Reader, obj interface{}) error {
    ...
	return validate(obj)
}
```
