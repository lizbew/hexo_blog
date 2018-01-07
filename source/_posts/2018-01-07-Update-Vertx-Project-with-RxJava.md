---
layout: post
title: 用RxJava 改造Vertx Project
date: 2018-01-07 11:23:39
tags: [vertx, rxjava]
---

早上花点时间修改 [wafer-java-session](https://github.com/lizbew/wafer-java-session/tree/rxjava)， 引入了RxJava， 保存在新的分支rxjava。

## 新增Maven 依赖

```xml
        <dependency>
            <groupId>io.vertx</groupId>
            <artifactId>vertx-rx-java</artifactId>
            <version>3.5.0</version>
        </dependency>
```

## 代码的修改

### MainVerticle

1. `MainVerticle` 的父类由 `io.vertx.core.AbstractVerticle` 改为 `io.vertx.rxjava.core.AbstractVerticle`

2. Verticle Deployment的变化
```java
Future<String> dbserviceDeployment = Future.future();
vertx.deployVerticle(SessionDatabaseVerticle.class.getName(), dbserviceDeployment.completer());
```
   修改为：
```java
Single<String> dbserviceDeployment = vertx.rxDeployVerticle(SessionDatabaseVerticle.class.getName());
dbserviceDeployment.flatMap(...)
    .subscribe(id -> startFuture.complete(), startFuture::fail);
```

### Service 相关的改动

* 接口`SessionDatabaseService`上新增注解`@VertxGen`， 两个静态方法create/createProxy 新增注解`@GenIgnore`。 新增注解的作用是生成rxjava相关的代理类。

* `SessionDatabaseService.createProxy()` 返回类型使用rxjava包里的。
```java
static SessionDatabaseService createProxy(Vertx vertx, String address) {
    return new SessionDatabaseServiceVertxEBProxy(vertx, address);
}
```
   修改为：
```java
@GenIgnore
static com.viifly.wafer.database.rxjava.SessionDatabaseService createProxy(Vertx vertx, String address) {
    return new com.viifly.wafer.database.rxjava.SessionDatabaseService(new SessionDatabaseServiceVertxEBProxy(vertx, address));
}
```

*  对`SessionDatabaseService`的方法调用都改为添加*rx*前缀的。

## 参考

* [Vert.x RxJava](http://vertx.io/docs/vertx-rx/java/)
* [guide to Vert.x for Java developers](http://vertx.io/docs/guide-for-java-devs/)

