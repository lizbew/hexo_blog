---
title: redis中存取protobuf编码的值， 使用lettuce库
date: 2020-02-03 11:40:48
tags: [redis, protobuf, lettuce, java]
---

需求： 经常的配置项对象需要存储在Redis中，值使用protobuf来序列化。Java库使用lettuce。 

相比使用redis存取string与hash, 使用protobuf序列化存取需要将整个对象一起存取， 存之前先使用protobuf序列化为byte[]，再按string存； 读操作时先读byte[]，再使用protobuf 反序列化为对象。

## java中使用protobuf

### 创建proto文件
先创建proto文件来定义message, 内容如下。 先是申明使用proto3； 接下来两个option， java_package 指定生成java文件所在的package, 而java_outer_classname是proto文件对应的外层class名。 通常一个proto文件中都会包含多个message的申请，给每个message生成的class都是外层class的子类。

```protobuf
syntax = "proto3";

option java_package = "com.viifly.test.proto";
option java_outer_classname = "ConfigProto";

message DogConfig {
   string name = 1;
   int32 age = 2;
   bool adopted = 3;
}
```
将文件保存在maven项目中 src/main/proto/config.proto中.  项目结构可以参考 https://www.xolstice.org/protobuf-maven-plugin/usage.html.

### 配置maven插件 

然后在pom.xml中添加protoc插件, 在编译时自动生成java 代码。

```xml
<dependencies>
    ...
    <dependency>
        <groupId>com.google.protobuf</groupId>
        <artifactId>protobuf-java</artifactId>
        <version>3.11.0</version>
    </dependency>
</dependencies>

<build>
    <extensions>
        <extension>
            <groupId>kr.motd.maven</groupId>
            <artifactId>os-maven-plugin</artifactId>
            <version>1.6.2</version>
        </extension>
    </extensions>
    <plugins>
        <plugin>
            <groupId>org.xolstice.maven.plugins</groupId>
            <artifactId>protobuf-maven-plugin</artifactId>
            <version>0.6.1</version>
            <configuration>
                <protocArtifact>
                    com.google.protobuf:protoc:3.11.0:exe:${os.detected.classifier}
                </protocArtifact>
            </configuration>
            <executions>
                <execution>
                    <goals>
                        <goal>compile</goal>
                        <goal>test-compile</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

### 使用protobuf 序列化

由protobuf message生成的类都不能直接使用new来创建，而是使用builder。先调用`.newBuilder()`来创建builder对象，设置字段值之后， 再调用`.build()`生成对象。 

`dogConfig.toByteArray()`将对象序列化为byte数组， `ConfigProto.DogConfig.parseFrom(byte[] data)` 从byte[]反序列化为对象。 

```java
import com.google.protobuf.InvalidProtocolBufferException;
import com.viifly.test.proto.ConfigProto;

public class ProtobufTest {
    public static void main(String[] args) throws InvalidProtocolBufferException {
        // 创建DogConfig 对象
        ConfigProto.DogConfig dogConfig= ConfigProto.DogConfig.newBuilder()
                .setName("huahua")
                .setAge(3)
                .setAdopted(true)
                .build();
        System.out.println("dogConfig = " + dogConfig.toString());

        // 序列化为byte[]
        byte[] data = dogConfig.toByteArray();
        System.out.println("data length = " + data.length);

        // 反序列化为DogConfig
        ConfigProto.DogConfig dogConfig2 = ConfigProto.DogConfig.parseFrom(data);
        System.out.println("dogConfig2 = " + dogConfig2.toString());

    }
}
```


## 使用lettuce库简单读写redis

### 启动redis实例

这里使用了docker来运行redis， 镜像来源为 https://hub.daocloud.io/repos/beb958f9-ffb6-4f68-817b-c17e1ff476c3。 
docker run的命令行添加了参数 `-p 6379:6379`， 将docker暴露的6379端口映射为本地端口，然后就可以用`localhost:6379`来访问了。

```bash
# 运行， 映射6379端口
docker run --name redis6379 -p 6379:6379 -d daocloud.io/library/redis

# 停止
docker stop redis6379
# 删除
docker rm redis6379
```

### 引入lettuce库

lettuce 是基于netty实现的redis客户端操作库，高效的异步实现。 先引入maven依赖，再写个简单的java程序。 

```xml
<dependency>
    <groupId>io.lettuce</groupId>
    <artifactId>lettuce-core</artifactId>
    <version>5.2.1.RELEASE</version>
</dependency>
```

先创建`RedisClient`对象，再创建connection, `connection.sync()`获取同步的读写`RedisStringCommands`, 然后get、set.
代码中使用单机redis，如果使用redis cluster则需要使用`RedisClusterClient`。

```java
import io.lettuce.core.RedisClient;
import io.lettuce.core.api.StatefulRedisConnection;
import io.lettuce.core.api.sync.RedisStringCommands;

public class RedisTest {
    public static void readRedis0() {
        RedisClient client = RedisClient.create("redis://localhost");
        StatefulRedisConnection<String, String> connection = client.connect();
        RedisStringCommands<String, String> sync = connection.sync();
        sync.set("key", "value00-1");

        String value = sync.get("key");
        sync.mget("abc", "key");
        System.out.println(value);
    }
}
```
从如上代码中`connect()`返回的结果类型为`StatefulRedisConnection<String, String>`, 带有两个String类型的泛型参数。 查看connection方法的源代码，它调用了另一个重载的带参数`RedisCodec<K, V> codec`的connection()方法。 其中`RedisCodec`是对redis的保存的key/value做编解码的，默认是string类型。当我们需要使用protobuf来序列化时，就要用到这个`RedisCodec`。


```java
public StatefulRedisConnection<String, String> connect() {
    return connect(newStringStringCodec());
}
public <K, V> StatefulRedisConnection<K, V> connect(RedisCodec<K, V> codec);
```

lettuce库自带了几个`RedisCodec`实现， `StringCodec`支持key/value都为String, `ByteArrayCodec`的key/value为byte[], `ComposedRedisCodec`key与value使用不同的编解码来组合为一个。如下创建一个key为String类型， value为byte[]类型的codec。与我们的需求value 为protobuf序列化已经很接近了，只需要实现将protobuf 对象序列为byte[]实达到要求了。

```java
RedisCodec<String, byte[]> codec = RedisCodec.of(StringCodec.UTF8, ByteArrayCodec.INSTANCE)
```

关于protobuf的序列化， netty本身也是有相应的类`io.netty.handler.codec.protobuf.ProtobufEncoder` 与 `io.netty.handler.codec.protobuf.ProtobufDecoder`，可以用来参考实现。 只不过它们实现成了netty的handler。

### 自定义实现RedisCodec

考虑到用同一个RedisCodec能达到对不同的类进行编解码， 使用到了泛型， 重新实现了一个类 `ProtobufCodec`.

```java
import com.google.protobuf.MessageLite;
import io.lettuce.core.codec.RedisCodec;
import io.lettuce.core.codec.StringCodec;

import java.nio.ByteBuffer;


public class ProtobufCodec<T extends MessageLite> implements RedisCodec<String, T> {
    private final StringCodec keyCodec = StringCodec.UTF8;
    private final T prototype;

    private static final boolean HAS_PARSER;
    private static final byte[] EMPTY = new byte[0];

    static {
        boolean hasParser = false;
        try {
            // MessageLite.getParserForType() is not available until protobuf 2.5.0.
            MessageLite.class.getDeclaredMethod("getParserForType");
            hasParser = true;
        } catch (Throwable t) {
            // Ignore
        }

        HAS_PARSER = hasParser;
    }

    public ProtobufCodec(T prototype) {
        this.prototype = prototype;
    }

    public static <T extends MessageLite> ProtobufCodec<T> of(T prototype) {
        return new ProtobufCodec(prototype);
    }

    @Override
    public String decodeKey(ByteBuffer bytes) {
        return keyCodec.decodeKey(bytes);
    }

    @Override
    public T decodeValue(ByteBuffer bytes) {
        int remaining = bytes.remaining();

        if (remaining == 0) {
            return null;
        }

        byte[] b = new byte[remaining];
        bytes.get(b);

        try {
            if (HAS_PARSER) {
                return (T) prototype.getParserForType().parseFrom(b);
            } else {
                return (T) prototype.newBuilderForType().mergeFrom(b).build();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }


        return null;
    }

    @Override
    public ByteBuffer encodeKey(String key) {
        return keyCodec.encodeKey(key);
    }

    @Override
    public ByteBuffer encodeValue(T value) {
        if (value == null) {
            return ByteBuffer.wrap(EMPTY);
        }

        return ByteBuffer.wrap(value.toByteArray());
    }
}
```

### 使用ProtobufCodec

```java
    public static void readRedis1() {
        //创建redis 连接
        RedisClient client = RedisClient.create("redis://localhost");
        StatefulRedisConnection<String, ConfigProto.DogConfig> connection
                = client.connect(ProtobufCodec.of(ConfigProto.DogConfig.getDefaultInstance()));


        // set
        ConfigProto.DogConfig dogConfig = ConfigProto.DogConfig.newBuilder()
                .setName("huahua")
                .setAge(3)
                .setAdopted(true)
                .build();
        connection.sync().set("dog-01", dogConfig);

        // get
        ConfigProto.DogConfig dogConfig2 = connection.sync().get("dog-01");
        System.out.println(dogConfig2);

    }
```