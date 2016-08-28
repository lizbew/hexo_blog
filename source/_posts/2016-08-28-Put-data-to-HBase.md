---
title: Put data to HBase
date: 2016-08-28 16:19:56
tags:
- HBase
- python
- thrift
---

# 将股票数据存入HBase

使用的数据文件为[Setup single-node Hadoop and load stock data](/2016/08/24/Setup-single-node-Hadoop-and-load-stock-data/)
中从网易财经导出的csv文件，文件名为数据日期， 例如`2016-08-26.csv`。


## 创建HBase表

参考[The Apache HBase Shell](http://hbase.apache.org/book.html#shell), 可将命令存成文件，再由hbase shell执行。

表名`stock-data1`， 列簇`price`， 保存为文件 `create_stock_table_hbase.txt`:
{% codeblock %}
create 'stock-data1', 'price'
list 'stock-data1'
describe 'stock-data1'
exit
{% endcodeblock %}

执行:
{% codeblock lang:bash %}
$HBASE_HOME/bin/hbase shell ./create_stock_table_hbase.txt
{% endcodeblock %}


## python代码

实现的步骤：
* 打开文件，按行读取，再按逗号`,`分割成字段列表。
* 根据第一行各列名称生成dict, 加入由文件名得到的日期。
* 转换成HBase接口的TPut数据结构，调用HBase thrift接口。 rowid: `<stock-symbol>:<date>`

使用到的thrift结构与函数：
* 结构: `TPut`, `TColumnValue`
* 函数: `THBaseService.Client.put()`

**注意**： `hbase.thrift`中声明的row, value都是`binary`，在python 2.7的代码都需要转成`str`， 字符串使用utf-8编码。

{% codeblock lang:python %}
def import_stock_data(hbase_client, data_file):
    data_date = os.path.splitext(os.path.basename(data_file))[0]

    f = codecs.open(data_file, 'r', encoding='utf-8')
    header_cols = f.readline().strip().split(',')

    column_labels = 'SYMBOL,NAME,PRICE,PERCENT,UPDOWN,OPEN,YESTCLOSE,HIGH,LOW,VOLUME,TURNOVER'.split(',')
    column_family = 'price'

    for line in f:
        if not line:
            continue
        cols = line.strip().split(',')
        #if cols[0] == 'SYMBOL':
        #   continue
        d = dict(zip(header_cols, cols))
        rowid = '{}:{}'.format(d['SYMBOL'], data_date)
        values = []
        values.append(TColumnValue(column_family, 'DATE', data_date))
        for c in column_labels:
            values.append(TColumnValue(column_family, c, codecs.encode(d.get(c), 'utf-8')))
        put_data = TPut(rowid, values)
        hbase_client.put('stock-data1', put_data)
    print 'import %s done' % data_file
{% endcodeblock %}
