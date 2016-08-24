---
layout: post
title: "从IE里导出SSL证书到JVM里"
description: ""
category: web
tags: [ssl, keytool]
---

原始发布于： http://blog.viifly.com/blog/posts/5001

**从IE里导出证书**

通过如下菜单可以打开IE的证书窗口：Tools->'Internet Options' ->Content->Certificates。 选择要导出的证书后，点击"Export...", 会开始导出向导。导出文件格式选择DER encoded binary X.509(.CER)，导出的文件名将以.cer结尾。

**将证书入JVM**

导入JVM可以由JDK自带的工具keytool来完。Java的keystore存放路径为`%JAVA_HOME%/lib/security/cacerts`，默认密码为*changeit*.

 - import
<pre><code>[jdk_path]\jre\bin>keytool -list -keystore ..\lib\security\cacerts
Enter keystore password: changeit
</code></pre>

 - list certs in keystore
<pre><code>[jdk_path]\jre\bin>keytool -import -keystore ..\lib
\security\cacerts -alias vkTestCer -file c:\sd.cer
Enter keystore password:
</code></pre>

 - Reference page1:  http://www.java-samples.com/showtutorial.php?tutorialid=210
 - Oracle Docs: http://docs.oracle.com/javase/7/docs/technotes/tools/windows/keytool.html


