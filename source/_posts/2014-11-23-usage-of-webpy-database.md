---
layout: post
title: "使用web.py访问数据库"
description: "usage of web.db database, and also read its code"
category: python
tags: [webpy, python, database]
---

web.py提供了基本的数据库访问封装，`web.database`，可以实现常用的数据库操作，但不能称为ORM。web.py cookbook里展示了常用的功能， 参见http://webpy.github.io/cookbook/,可以以此为起点来了解web.database使用，进而学习其源码。

## 数据库链接对象

{% codeblock lang:python %}
import web

db = web.database(dbn='mysql', db='dbname', user='foo')
print db.select('foo', where='id=1')
{% endcodeblock %}

函数`web.database(dbn, **kws)`初始化并返回一个数据库连接，当需要连接多个数据库时多次调用即可。参数dbn是数据库类型，源码(web/db.py, register_database)显示可使用的值有:mysql, postgres, sqlite, firebird, mssql, oracle。

## 数据库访问操作

首先来看下select：


{% codeblock lang:python %}
# Select all entries from table 'mytable'
entries = db.select('mytable', where='id=1')
{% endcodeblock %}

传给`select()`的第一个参数是数据库表名， 用关键字参数`where`传递SQL的where子句。除了表名之外，SQL查询语句的其它部分都是通过关键字参数传递给`select()`。以下是`select()`支持的其它参数关键字列表。其中`_test=True`时select返回是生成的SQL语句，而非查询结果。

* vars - where子句中的变量，实现绑定变量
{% codeblock lang:python %}
myvar = dict(name="Bob")
results = db.select('mytable', myvar, where="name = $name")
{% endcodeblock %}
* what - select返回的列，默认是`*`: `results = db.select('mytable', what="id,name")`
* where
* order
* group
* limit
* offset
* _test

类似的，`db.insert()`, `db.update()`, `db.delete()`的第一个参数都是数据库表名，其它部分由关键字参数传递。

{% codeblock lang:python %}
# Insert an entry into table 'mytable'
sequence_id = db.insert('mytable', firstname="Bob",lastname="Smith",joindate=web.SQLLiteral("NOW()"))

# update 
db.update('mytable', where="id = 10", value1 = "foo")

#delete
db.delete('mytable', where="id=10")
{% endcodeblock %}

另外还有个`db.query()`，接受SQL语句字符串作为参数，也支持关键字参数vars的绑定变量和_test。

{% codeblock lang:python %}
db = web.database(dbn='postgres', db='mydata', user='dbuser', pw='')

results = db.query("SELECT COUNT(*) AS total_users FROM users")
print results[0].total_users # -> prints number of entries in 'users' table

# use with vars
results = db.query("SELECT * FROM users WHERE id=$id", vars={'id':10})
{% endcodeblock %}

## select()/query()的返回结果

select()/query()的返回结果类型为`iterbetter`的迭代器， 每一行的数据为一个dict。 iterbetter定义在中web/utils.py，支持以数组方式`result[i]`访问。

## 支持事务(transaction)

webpy database也是支持事务的，也可嵌套（除sqllit）。具体参见http://webpy.github.io/cookbook/transactions，以下部分也摘自该处。

基本使用模式：

{% codeblock lang:python %}
import web

db = web.database(dbn="postgres", db="webpy", user="foo", pw="")
t = db.transaction()
try:
    db.insert('person', name='foo')
    db.insert('person', name='bar')
except:
    t.rollback()
    raise
else:
    t.commit()
{% endcodeblock %}

在python2.5+环境下可在`with`语句使用：

{% codeblock lang:python %}
from __future__ import with_statement

db = web.databse(dbn="postgres", db="webpy", user="foo", pw="")

with db.transaction():
    db.insert('person', name='foo')
    db.insert('person', name='bar')
{% endcodeblock %}

web.py database并未实现ORM，但可使用sqlalchemy, 详情见http://webpy.github.io/cookbook/sqlalchemy。

## 源码web/db.py

web.py database相关的代码可以直接在Github上查看[https://github.com/webpy/webpy/blob/master/](https://github.com/webpy/webpy/blob/master/)。

入口函数是`database()`, 它根据dbn从dict里查找对应类型数据库的实现类，再用接受到的参数将其初始化。

数据库基类为`class DB`，实现了对数据库访问操作, 都是先根据参数生成SQL语句，再由数据库接口执行SQL得到结果。对应于不同类型的数据库，`DB`的子类有: MySQLDB, PostgresDB, SqliteDB, FirebirdDB, MSSQLDB, OracleDB. 映射关系保存在`_databases = {}`中；统一通过函数`def register_database(name, clazz)`添加，例如：

{% codeblock lang:python %}
register_database('mysql', MySQLDB)
{% endcodeblock %}

在db.py的开始部分先定义了几个异常类，接着是生成SQL语句用到的辅助类和函数。生成SQL的辅助类有：

* SQLParam
* SQLQuery
* SQLLiteral

函数有：

* _sqllist(values)
* reparam(string_, dictionary)
* sqlify(obj)
* sqllist(lst) - _sqllist返回的结果可能会带'()',而sqllist没有
* sqlors(left, lst)
* sqlwhere(dictionary, grouping=' AND ')
* sqlquote(a)

事务的类为`Transaction`, 接下来定义`class DB`及其子类。

