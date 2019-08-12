---
title: 安装 prometheus 和 Grafana
date: 2019-08-08 00:01:42
tags: [prometheus, Grafana]
---

在树莓派上尝试安装了prometheus 和 Grafana， pi 3 Model B+, 下载安装包版本选了armv7.

## prometheus

prometheus的访问地址为localhost:9090. node_exporter 用来采集linux系统中一些基本指标， 监听端口为9100，在prometheus.yml中添加scrape_configs下一个job_name就可以开始上报。

* https://prometheus.io/download/

* https://github.com/prometheus/node_exporter
* https://github.com/prometheus/pushgateway

## grafana

* 安装指南 https://grafana.com/docs/installation/debian/
* https://grafana.com/grafana/download?platform=arm

```bash
wget https://dl.grafana.com/oss/release/grafana_6.3.2_armhf.deb
sudo apt-get install -y adduser libfontconfig
# sudo apt --fix-broken install  ## may need this
sudo dpkg -i grafana_6.3.2_armhf.deb 

## start/stop
sudo /bin/systemctl start grafana-server
sudo /bin/systemctl stop grafana-server
```

grafana中添加prometheus数据源:
* https://prometheus.io/docs/visualization/grafana/
* https://grafana.com/docs/features/datasources/prometheus/

![架构图](/images/post/2019-08-12/grafana-view.png)
