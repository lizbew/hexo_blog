---
title: setup minikube in macos
date: 2019-06-12 23:41:38
tags: [minikube, macos] 
---

记录一下安装minikube的过程。 源起于无法安装golang工具包，没有VPN可以访问的。看到circleci上有提供golang构建工具的image, 于是想起可以在机器上安装docker，再安装golang相关的docker image, 然后就有golang环境了。。

* 参考网页  https://kubernetes.io/docs/tasks/tools/install-minikube/
* github页 https://github.com/kubernetes/minikube

## 安装 hyperkit驱动

先使用`brew` 安装 hyperkit

```bash
brew install hyperkit
```

再安装minikube相关的驱动 

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/docker-machine-driver-hyperkit \
&& sudo install -o root -g wheel -m 4755 docker-machine-driver-hyperkit /usr/local/bin/
```

使用驱动：

```bash
minikube start --vm-driver hyperkit
minikube config set vm-driver hyperkit
```

## 安装 minikube

安装成功之后， 运行命令位于 `/usr/local/bin/minikube`

```bash
brew cask install minikube
brew install kubernetes-cli
```

## minikube 初体验

```bash
# start
minikube config set vm-driver hyperkit
minikube start

# add deployment
kubectl run hello-minikube --image=k8s.gcr.io/echoserver:1.10 --port=8080
kubectl expose deployment hello-minikube --type=NodePort
kubectl get pod
minikube service hello-minikube --url
# then visit in browser

# delete
kubectl delete services hello-minikube
kubectl delete deployment hello-minikube
minikube stop
# run below to delete status
#minikube delete
```

## 新增学习资源

* https://github.com/caicloud/kube-ladder/blob/master/tutorials/lab2-application-and-service.md