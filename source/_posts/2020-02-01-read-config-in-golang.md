---
title: golang中读取配置文件
date: 2020-02-01 21:51:00
tags: [golang, config, ini, json, toml]
---


# 读取ini文件格式

ini文件是比较常用的配置文件格式，字符串表示的键值对，还可以使用section来区分不同的块， 可以有一个默认块。如下一个示例配置文件`cfg_ini.ini`的内容：

```ini
appName=Test One

[http]
host=localhost
```

golang中可以使用包`github.com/go-ini/ini`来读取ini文件。

```go
import (
	"fmt"
	"log"

	"github.com/go-ini/ini"
)

func read_ini() {
	var err error
	var cfgFile *ini.File
	cfgFile, err = ini.Load("cfg_ini.ini")
	if err != nil {
		log.Fatalf("Failed to open file: %v", err)
		return
	}

	appName := cfgFile.Section("").Key("appName").String()
	host := cfgFile.Section("http").Key("host").MustString("")

	fmt.Printf("appName=%s, http/host=%s\n", appName, host)

}
```

# 读取toml文件

toml文件格式是在rust语言中使用比较多的，相比ini支持map\list等数据类型。 这里使用库`github.com/BurntSushi/toml`。

```toml
#cfg.toml
mongo_url = "mongodb://127.0.0.1:27017"
account_info = ""
```

```go
import (
	"fmt"

	"github.com/BurntSushi/toml"
)

type serverConfig struct {
	MongoUrl    string `toml:"mongo_url"`
	AccountInfo string `toml:"account_info"`
}

func read_toml() {
	var config serverConfig

	if _, err := toml.DecodeFile("cfg.toml", &config); err != nil {
		fmt.Printf("Parse config [cfg.toml] error: %s\n", err)
		return
	}
	fmt.Printf("mongo_url = %s", config.MongoUrl)
}
```

# 读json

golang标准库包含对json的读写库 `encoding/json`, 直接拿来使用。

```json
{
    "name": "test app",
    "age": 1
}
```

```golang
import (
	"encoding/json"
	"fmt"
	"log"
	"os"
)

type MyConfig struct {
	Name string `json:"name"`
	Age  int    `json:"age"`
}

func read_json() {
	var cfg MyConfig

	file, err := os.Open("cfg.json")
	if err != nil {
		log.Fatalf("Failed to open file cfg.json, %v", err)
		return
	}

	json.NewDecoder(file).Decode(&cfg)
	fmt.Printf("name=%s\n", cfg.Name)
}
```