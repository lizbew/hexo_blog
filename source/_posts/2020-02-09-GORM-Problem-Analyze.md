---
title: 使用GORM过程中遇到的坑，以及源代码分析
date: 2020-02-09 16:41:04
tags: [gorm, golang]
---

GORM是golang下的ORM框架，处理golang struct与数据库结构之间的映射，能根据struct结构自动生成SQL, 方便的CRUD操作，并且支持表关联。 官方网址 http://gorm.io/zh_CN/docs/index.html

## 发现问题, Find()方法使用的表名不正确


发现的坑来源于下面的代码。相较于GORM的示例代码，用`TableName()`设备表名为`hax_products`， 同时设置`gorm.DefaultTableNameHandler`给默认生成的表名添加前缀`hax_`， 并且使用`db.LogMode(true)`打印SQL日志。

主要目的是测试： 当显式设置了表名，并且有指定默认表名前缀时， 默认表名前缀是否会被再次添加。

这里gorm 使用的版本为`1.9.11`. 在glide.lock中的version值为79a77d771dee4e4b60e9c543e8663bbc80466670。 

```go
package main

import (
	"fmt"

	"github.com/jinzhu/gorm"
	//_ "github.com/jinzhu/gorm/dialects/sqlite"
	_ "github.com/mattn/go-sqlite3"
)

type Product struct {
	gorm.Model
	Code  string
	Price uint
}

func (Product) TableName() string {
	return "hax_products"
}

func main() {
	db, err := gorm.Open("sqlite3", "test.db")
	if err != nil {
		panic("failed to connect database")
	}
	defer db.Close()

	gorm.DefaultTableNameHandler = func(db *gorm.DB, defaultTableName string) string {
		return "hax_" + defaultTableName
	}

	db.LogMode(true)

	// Migrate the schema
	db.AutoMigrate(&Product{})
	db.Create(&Product{Code: "L1212", Price: 1000})

	var product Product
	db.First(&product, 1)

	var products []Product
	db.Find(&products)
	fmt.Printf("Total count %d", len(products))
}
```

运行之后输出结果如下：

![gorm error](/images/post/2020-02-09/gorm-error.png)


可以看到，创建语言及查询单个记录时表名为`hax_products`，而查询列表时使用的表名为`hax_hax_products`且抛出了表名不存在异常。 查询单个记录时使用了`TableName()`返回的表名，而在查询结果为Array时，表名在`TableName()`的基础上又添加了前缀。


## 源代码分析

网上有不少GORM源代码分析的文章可以用来参考。 GORM 主要分析如下几个struct结构体。

* `type DB struct` (gorm/main.go)代表数据库连接，每次操作数据库会创建出clone对象。 方法`gorm.Open()`返回的值类型就是这个结构体指针。
* `type Scope struct` (gorm/scope.go) 当前数据库操作的信息，每次添加条件时也会创建clone对象。
* `type Callback struct` (gorm/callback.go) 数据库各种操作的回调函数， SQL生成也是靠这些回调函数。 每种类型的回调函数放在单独的文件里，比如查询回调函数在gorm/callback_query.go， 创建的在gorm/callback_create.go

为定位表名生成的代码在哪个文件，分析从`db.First()` 与 `db.Find()`入手。

### db.First() 代码分析

`First()`方法位于gorm/main.go文件中， `.callCallbacks(s.parent.callbacks.queries)`调用了query回调函数。

```go
// file: gorm/main.go
// First find first record that match given conditions, order by primary key
func (s *DB) First(out interface{}, where ...interface{}) *DB {
	newScope := s.NewScope(out)
	newScope.Search.Limit(1)

	return newScope.Set("gorm:order_by_primary_key", "ASC").
		inlineCondition(where...).callCallbacks(s.parent.callbacks.queries).db
}
```

`Callback`结构体中定义queries为函数指针数组， 而默认值的初始化在gorm/callback_query.go的`init()`方法中， 查询方法为`queryCallback`, 而`queryCallback()`方法又调用到`scope.prepareQuerySQL()`, scope中的方法真正生成SQL的地方。

```go
// file: gorm/callback.go
type Callback struct {
	logger     logger
	creates    []*func(scope *Scope)
	updates    []*func(scope *Scope)
	deletes    []*func(scope *Scope)
	queries    []*func(scope *Scope)
	rowQueries []*func(scope *Scope)
	processors []*CallbackProcessor
}

// file: gorm/callback_query.go
// Define callbacks for querying
func init() {
	DefaultCallback.Query().Register("gorm:query", queryCallback)
	DefaultCallback.Query().Register("gorm:preload", preloadCallback)
	DefaultCallback.Query().Register("gorm:after_query", afterQueryCallback)
}

// queryCallback used to query data from database
func queryCallback(scope *Scope) {
...
    scope.prepareQuerySQL()
...
}
```

跟踪代码到scope.go文件， 函数`TableName()`是获取数据库表名的地方。 它按如下顺序来确定表名：

1. scope.Search.tableName 查询条件中设置了表名， 则直接使用
2. scope.Value.(tabler) 值对象实现了`tabler`接口(方法`TableName() string`), 则从调用方法获取 
3. scope.Value.(dbTabler) 值对象实现了`dbTabler`接口(方法`TableName(*DB) string`), 则从调用方法获取 
4. 若以上条件都不成立，则从`scope.GetModelStruct()`中获取对象的结构体信息，从结构体名生成表名

对比以上条件， 示例中的`Product`结构体定义了方法`TableName() string`，符合条件2，那么`db.First(&product, 1)`使用的表名就是`hax_products`。

```go
// file: gorm/scope.go
func (scope *Scope) prepareQuerySQL() {
	if scope.Search.raw {
		scope.Raw(scope.CombinedConditionSql())
	} else {
		scope.Raw(fmt.Sprintf("SELECT %v FROM %v %v", scope.selectSQL(), scope.QuotedTableName(), scope.CombinedConditionSql()))
	}
	return
}

// QuotedTableName return quoted table name
func (scope *Scope) QuotedTableName() (name string) {
	if scope.Search != nil && len(scope.Search.tableName) > 0 {
		if strings.Contains(scope.Search.tableName, " ") {
			return scope.Search.tableName
		}
		return scope.Quote(scope.Search.tableName)
	}

	return scope.Quote(scope.TableName())
}

// TableName return table name
func (scope *Scope) TableName() string {
	if scope.Search != nil && len(scope.Search.tableName) > 0 {
		return scope.Search.tableName
	}

	if tabler, ok := scope.Value.(tabler); ok {
		return tabler.TableName()
	}

	if tabler, ok := scope.Value.(dbTabler); ok {
		return tabler.TableName(scope.db)
	}

	return scope.GetModelStruct().TableName(scope.db.Model(scope.Value))
}
```

### db.Find() 代码分析

`Find()`代码如下，与`First()`同样是使用了`.callbacks.queries`回调方法，不同点在于设置了`newScope.Search.Limit(1)`只返回一个结果、增加了按id排序。

```go
// Find find records that match given conditions
func (s *DB) Find(out interface{}, where ...interface{}) *DB {
	return s.NewScope(out).inlineCondition(where...).callCallbacks(s.parent.callbacks.queries).db
}
```

在debug模式下跟踪代码到`scope.TableName()`中时，两次查询的区别显示出来了： 它们的结果值类型不同。 
`db.First(&product, 1)`的值类型为结构体的指针`*Product`，而`db.Find(&products)`的值类型是数组的指针`*[]Product`， 从而导致`db.Find(&products)`进入条件4，需要靠分析struct结构体来生成表名。

```go
// file: gorm/model_struct.go
// TableName returns model's table name
func (s *ModelStruct) TableName(db *DB) string {
	s.l.Lock()
	defer s.l.Unlock()

	if s.defaultTableName == "" && db != nil && s.ModelType != nil {
		// Set default table name
		if tabler, ok := reflect.New(s.ModelType).Interface().(tabler); ok {
			s.defaultTableName = tabler.TableName()
		} else {
			tableName := ToTableName(s.ModelType.Name())
			db.parent.RLock()
			if db == nil || (db.parent != nil && !db.parent.singularTable) {
				tableName = inflection.Plural(tableName)
			}
			db.parent.RUnlock()
			s.defaultTableName = tableName
		}
	}

	return DefaultTableNameHandler(db, s.defaultTableName)
}
```

默认表名`s.defaultTableName`为空值时先进行求值，`reflect.New(s.ModelType).Interface().(tabler)`先判断是否实现了`tabler`接口，有则调用其TableName()取值； 否则的话从结构体的名字来生成表名。 结果返回之前再调用 `DefaultTableNameHandler(db, s.defaultTableName)`方法。

这个`ModelStruct`的TableName方法与`scope.TableName()` 中的逻辑两个不一致的地方：

1. `scope.TableName()`会判断是否实现`tabler`与`dbTabler`两个接口，而这里只判断了`tabler`
2. `scope.TableName()` 是将tableName结果直接返回的， 而这里多调用了`DefaultTableNameHandler()`。

因为逻辑2的存在， 当重写了`DefaultTableNameHandler()`方法时， 就会出现表前缀再次被添加了表名前。

## 另一个坑： DefaultTableNameHandler()在多数据库时出现混乱

通过以上代码的分析，于是发现了另一个坑： 当一个程序中使用两个不同的数据库时， 重写方法`DefaultTableNameHandler()`会影响到两个数据库中的表名。 其中一个数据库需要设置表前缀时，访问另一个数据库的表也可能会被加上前缀。 因为是包级别的方法，整个代码里只能设置一次值。

```go
// file: gorm/model_struct.go
// DefaultTableNameHandler default table name handler
var DefaultTableNameHandler = func(db *DB, defaultTableName string) string {
	return defaultTableName
}
```

## 总结

* 当给结构体实现了`TableName()`方法时，就不要设置`DefaultTableNameHandler`了。 
* 保持所有Model的表名生成方式一致，要么全部使用自动生成的表名，要么全部实现`tabler`接口(实现`TableName()`方法)
* 当需要使用多个数据库时，要避免设置`DefaultTableNameHandler`
* __强烈建议： 所有Model结构体全部实现`tabler`接口__
