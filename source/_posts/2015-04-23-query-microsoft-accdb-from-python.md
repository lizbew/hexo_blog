---
layout: post
title: "query Microsoft Accdb from Python"
description: "Use pypyodbc to query Microsoft Access DB"
category: python
tags: [accdb, pypyodbc, mdb]
---

工作中的一项任务需要访问MS Access DB， 主要是导出一些表和数据。网上搜索了一番后，在stackoverflow上找到了答案。 其实挺简单的， 导入库pypyodbc，连接上*.accdb文件后， 就是普通Python DBAPI方式访问了。

* 主要参考了这篇 [How do I import an .accdb file into Python and use the data?](http://stackoverflow.com/questions/25820698/how-do-i-import-an-accdb-file-into-python-and-use-the-data)
* pypyodbc [https://pypi.python.org/pypi/pypyodbc](https://pypi.python.org/pypi/pypyodbc)
* 我自已写的代码在[这里](https://github.com/lizbew/code-practice/blob/master/import_accdb_table_to_oracle.py)

下面代码来自 stackoverflow:

{% codeblock lang:python %}
# -*- coding: utf-8 -*-
import pypyodbc
pypyodbc.lowercase = False
conn = pypyodbc.connect(
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
    r"Dbq=C:\Users\Public\Database1.accdb;")
cur = conn.cursor()
cur.execute("SELECT CreatureID, Name_EN, Name_JP FROM Creatures");
while True:
    row = cur.fetchone()
    if row is None:
        break
    print(u"Creature with ID {0} is {1} ({2})".format(
        row.get("CreatureID"), row.get("Name_EN"), row.get("Name_JP")))
cur.close()
conn.close()
{% endcodeblock %}

## 如何得到所有表和表的列名？

通过调用`cursor`对象的如下两个方法即可实现。 它们是代替`cursor.execute()`调用，再调用`cursor.fetchone()`访问各行数据。

* cur.tables()
* cur.columns(table)

