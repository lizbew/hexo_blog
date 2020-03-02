---
title: seed-rs quickstart 简化版
date: 2020-03-01 12:57:49
tags: [seed-rs, rust, wasm]
---

[seed-rs](https://github.com/seed-rs/seed) 是rustlang实现的web前端开发框架，编译成[wasm](https://github.com/rustwasm/wasm-bindgen)之后在浏览器上运行； 代码架构上仿照[Elm](https://guide.elm-lang.org/architecture/)， 函数式语言的风格来实现UI。 编码风格的解释可以参考文章 https://www.infoq.cn/article/Mq07yGgEhhW7xASNfEsT。 本文是seed-rs [quickstart](https://seed-rs.org/guide/quickstart)的简明版。

## 环境安装

1. 第一步是要先安装rust环境, 参考rust官方文档， 运行如下命令一行搞定。

  `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

  seed-rs需要最新的rust-lang环境， 如果是之前已经安装过了， 升级用`rustup update`。
2. 安装wasm32-unknown-unknown编码目标： `rustup target add wasm32-unknown-unknown`
3. 安装cargo-make： `cargo install --force cargo-make`

## 极简启动方式

seed-rs在github提供了example代码可以直接clone下来运行， `git clone https://github.com/seed-rs/seed-quickstart.git`。  

在项目目录中运行 `cargo make build` 来build， `cargo make serve` 启动开发服务，监听在 127.0.0.0:8000。 如果需要监听代码变化， 并自动构建的话， 运行 `cargo make watch`。 

## 从新开始创建项目

本文的主要内容还是从新开始创建项目。 运行命令 `cargo new --lib appname` 来创建一个新的lib 项目， 其中`appname`是项目名称，请自行更改。

然后在项目目录下新建`index.html`， body标签中包含如下内容。 标签位置`id="app"`是代码运行之后内容渲染展示的位置， 和react/vue.js等类似的。

```html
<section id="app"></section>
<script type="module">
    import init from '/pkg/package.js';
    init('/pkg/package_bg.wasm');
</script>
```

`Cargo.toml`是创建项目时自动生成的文件，管理项目信息和三方依赖包等， 如同nodejs中的package.json。 在其中添加需要的依赖 `asm-bindgen`,`web-sys`, `seed`。 crate-type 项的值设置为 `"cdylib"`。 

```toml
[package]
name = "appname"
version = "0.1.0"
authors = ["Your Name <email@address.com>"]
edition = "2018"

[lib]
crate-type = ["cdylib"]

[dependencies]
seed = "^0.6.0"
wasm-bindgen = "^0.2.50"
```

## 在lib.rs中添加代码

lib.rs中库类型项目的主程序文件, 内容如下。 代码是Elm风格的架构，相关的概念主要是： Model, Msg, View, Update。 

```rust
use seed::{*, prelude::*};

// Model

struct Model {
    count: i32,
    what_we_count: String
}

// Setup a default here, for initialization later.
impl Default for Model {
    fn default() -> Self {
        Self {
            count: 0,
            what_we_count: "click".into()
        }
    }
}


// Update

#[derive(Clone)]
enum Msg {
    Increment,
    Decrement,
    ChangeWWC(String),
}

/// How we update the model
fn update(msg: Msg, model: &mut Model, _orders: &mut impl Orders<Msg>) {
    match msg {
        Msg::Increment => model.count += 1,
        Msg::Decrement => model.count -= 1,
        Msg::ChangeWWC(what_we_count) => model.what_we_count = what_we_count,
    }
}


// View

/// A simple component.
fn success_level(clicks: i32) -> Node<Msg> {
    let descrip = match clicks {
        0 ..= 5 => "Not very many 🙁",
        6 ..= 9 => "I got my first real six-string 😐",
        10 ..= 11 => "Spinal Tap 🙂",
        _ => "Double pendulum 🙃"
    };
    p![ descrip ]
}

/// The top-level component we pass to the virtual dom.
fn view(model: &Model) -> impl View<Msg> {
    let plural = if model.count == 1 {""} else {"s"};

    // Attrs, Style, Events, and children may be defined separately.
    let outer_style = style!{
            St::Display => "flex";
            St::FlexDirection => "column";
            St::TextAlign => "center"
    };

    div![ outer_style,
        h1![ "The Grand Total" ],
        div![
            style!{
                // Example of conditional logic in a style.
                St::Color => if model.count > 4 {"purple"} else {"gray"};
                St::Border => "2px solid #004422"; 
                St::Padding => unit!(20, px);
            },
            // We can use normal Rust code and comments in the view.
            h3![ format!("{} {}{} so far", model.count, model.what_we_count, plural) ],
            button![ simple_ev(Ev::Click, Msg::Increment), "+" ],
            button![ simple_ev(Ev::Click, Msg::Decrement), "-" ],

            // Optionally-displaying an element
            if model.count >= 10 { h2![ style!{St::Padding => px(50)}, "Nice!" ] } else { empty![] }
        ],
        success_level(model.count),  // Incorporating a separate component

        h3![ "What are we counting?" ],
        input![ attrs!{At::Value => model.what_we_count}, input_ev(Ev::Input, Msg::ChangeWWC) ]
    ]
}


#[wasm_bindgen(start)]
pub fn render() {
    App::builder(update, view)
        .build_and_start();
}
```

## 运行项目

原文中还缺少一段关于运行`cargo make build`所需的`Makefile.toml`。 在运行make之前你肯定先有个Makefile才行，只不过cargo项目的Makefile文件是toml格式的。 可以直接从github中代码copy过来: https://github.com/seed-rs/seed-quickstart/blob/master/Makefile.toml

* build项目 `cargo make build`
* 本地运行 `cargo make serve`， 然后浏览器访问 127.0.0.1:8000
* build release版本 `cargo make build_release`， 生成的目标wasm文件会小很多
