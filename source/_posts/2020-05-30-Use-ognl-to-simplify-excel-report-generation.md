---
title: 借助OGNL来简化Excel报表生成
date: 2020-05-30 00:03:26
tags: [ognl, excel, poi, java, myBatis]
---

工作中需要导出数据生成Excel报表， 由Ant Design中Table配置参数设计了一简单的excel生成方案，解决了excel中单元格一个个来设置繁琐重复工作。 问题域也主要针对是的数据表的导出，内容表头再加上一行行的数据 ， 并没有复杂的格式。

And Design 中[Table](https://3x.ant.design/components/table-cn/#Table)组件最重要的两个参数是，columns与dataSource：

* columns 定义每个列的标题与数据展示格式， 其中对象的dataIndex是引用每行数据的key, 也可以指定render函数计算值
* dataSource则是一个列表，每一个元素会对应到表格中的一行 

在使用java生成excel的工具中也是使用了类似的设计。 为了excel中单元格数据的灵活性，值的生成需要使用使用表达式，当需要改变单元格内容时只需要修改表达式字符串。这里选用的OGNL表达式， 直接引用了myBatis库中的。 

## Maven 依赖

其中myBatis是因为要查询数据使用，并且刚好myBatis也有OGNL的支持，就借用了其中的类。 

```xml
    <dependency>
        <groupId>org.mybatis</groupId>
        <artifactId>mybatis</artifactId>
        <version>3.5.4</version>
    </dependency>

    <dependency>
        <groupId>org.apache.poi</groupId>
        <artifactId>poi</artifactId>
        <version>4.1.2</version>
    </dependency>

    <dependency>
        <groupId>org.apache.poi</groupId>
        <artifactId>poi-ooxml</artifactId>
        <version>4.1.2</version>
    </dependency>
```

## Column - 列的表示类

如下Column省略了get/set方法。 `title`是每列的标题， 而valueEl是计算单元格值的OGNL表示达， 也是一个字符串。

```java
public class Column {
    private String title;
    private String valueEl;

    public Column(String title, String valueEl) {
        this.title = title;
        this.valueEl = valueEl;
    }
    ...
}
```

`ValueEl`类则计算OGNL的值。参考了myBatis中TextSqlNode类的实现， 自己定义了`SimpleBindingTokenParser`。

```java
import org.apache.ibatis.parsing.GenericTokenParser;
import org.apache.ibatis.parsing.TokenHandler;
import org.apache.ibatis.scripting.xmltags.OgnlCache;

import java.util.Map;

public class ValueEl {

    public String apply(String text, Map<String, Object> context) {
        GenericTokenParser parser = createParser(new SimpleBindingTokenParser(context));
        return parser.parse(text);
    }

    private GenericTokenParser createParser(TokenHandler handler) {
        return new GenericTokenParser("${", "}", handler);
    }

    public static class SimpleBindingTokenParser implements TokenHandler{
        private Map<String, Object> context;

        public SimpleBindingTokenParser(Map<String, Object> context) {
            this.context = context;
        }

        @Override
        public String handleToken(String content) {
            Object value = OgnlCache.getValue(content, context);
            String srtValue = value == null ? "" : String.valueOf(value); // issue #274 return "" instead of "null"
            return srtValue;
        }
    }
}
```

## Excel的生成逻辑

生成逻辑就是几个循环了， 遍历columns生成表头，再遍历dataSource对应生成数据行，每其中的每个单元格调用OGNL表达式计算值再设置到cell中了。 

```java
    public <T> Workbook generate(List<Column> columns, List<T> dataSource) {
        SXSSFWorkbook workbook = new SXSSFWorkbook();
        Sheet sheet = createSheet(workbook, "Sheet1");

        CellStyle headerStyle = createHeaderStyle(workbook);
        int rowIndex = 0;

        fillHeaderRow(sheet.createRow(rowIndex++), columns, headerStyle);
        for (T record: dataSource) {
            fillDataRow(sheet.createRow(rowIndex++), columns, record, null);
        }

        return workbook;

    }

    private void fillDataRow(Row row, List<Column> columns, Object data, CellStyle style) {
        ValueEl valueEl = new ValueEl();
        for (int cellIndex = 0; cellIndex < columns.size(); cellIndex++) {

            Map<String, Object> context = new HashMap<>(2);
            context.put("record", data);

            String value = valueEl.apply(columns.get(cellIndex).getValueEl(), context);
            setCellString(row, cellIndex, value, style);
        }
    }
```

## 调用示例

注意下面`${record.val1}`, 每行的数据对象都是以`record`来引用的。

```java
List<Column> columns = new ArrayList<>(2);
columns.add(new Column("Val-A", "${record.val1}"));
columns.add(new Column("Val-B", "${record.val2}"));

List<TestModel> dataSource = new ArrayList<>(3);
dataSource.add(new TestModel("val1-tst", "val2-conte"));

ReportGenerator reportGenerator = new ReportGenerator();
Workbook workbook = reportGenerator.generate(columns, dataSource);
```