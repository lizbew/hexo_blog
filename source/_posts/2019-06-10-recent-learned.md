---
title: 总结一下最近的学习 201906
date: 2019-06-10 23:09:10
tags:
---

最近杂七杂八的看了点，缺少总结。技术能力还是有点欠缺，需要找个点突破提升。

1. Spring IOC的原理

    Spring IOC参照一本原码解析的书看了部分源码。 先思考框架解决的问题，使用的方案与策略， 再从网上其它途径了解流程、类关系图，然后再翻源码会容易理解。 一句话，先了解是做什么的，有个大概的思路，再去了解怎么实现 。

    对于IOC容器， 就是来取bean实例的。 (1)最原始的，就是先创建个bean实例放入容器， 需要的时候再从容器取；(2)往上一点， 就是只定义bean要怎么创建，给出相关的信息，交给容器来帮你创建，而创建的实例的策略又细分成只需创建一次和每次取时都创建一次等。 (1)就是singletone的实例， (2)就是BeanDefinition相关的了。 所以BeanFactory就是有同时支持singletone与beanDefintion， 从类的继承结构上也可以看出这一点来。

2.  Spring Security  参考网上博客了解大概原理， 怎么使用；还有oauth流程相关的。 在考虑直接使用auth0

    - https://github.com/auth0

3.  circleci 与 now

    circleci 是在github上了解的， 用于开源项目的CI/CD。相比较于jenkins， circleci的构建环境都使用了docker镜像， 免去了安装构建工具步骤。 CI/CD过程都是需要多种步骤组成来完成， CI/CD都需要某种流程编排引擎，circleci使用yaml来定义。

    now 能让你的前端页面直接部署在服务器上，对外提供服务。 这个工具是静态网站编译生成之后作用集成验证，也可以用来直接对外服务的。使用serverless相关的技术， 也是我觉得神奇的地方，吸引我最近开始了解serverless/faas的实现，加快个人应用开发。

    - https://github.com/circleci/circleci-docs
    - https://github.com/zeit/now-cli