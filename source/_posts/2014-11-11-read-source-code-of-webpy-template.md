---
layout: post
title: "试读webpy template源码"
description: ""
category: python
tags: [python, webpy, template]
---

这几天花了点时间读了下web.py的template代码，只是大概的过了下。主要想了解下Python中AST编译相关的模块使用方法。

先看个webpy template使用方法，来自其[cookbook](webpy.org/docs/0.3/templetor). 首先是template内容的html, 置于_./templates/hello.html_

{% codeblock lang:html %}
$def with (name)
Hello $name!
{% endcodeblock %}

在代码里初始化render, 传递文件夹名为参数，然后就可以调用和模板同名的方法了，生成的html以字符串返回。

{% codeblock lang:python %}
render = web.template.render('templates')
print render.hello('world')
{% endcodeblock %}

web.py template的语法格式同样参考其cookbook，变量赋值或语句都以$开始；$if/$for/$while都需要单独一行，内容行首遵循python的缩进格式。template内容是一行行处理的， 生成nodelist，转换成python代码，然后再调用python 编译服务。

看代码当然是从[github](https://github.com/webpy/webpy/blob/master/web/template.py)开始了， template 相关的代码在文件_ webpy / web / template.py
_. template的初始化是从`class Render`开始，由`render._load_template`,模板类是`class BaseTemplate`和`class Template`。模板的解析工作由`class Parser`进行， 解析后生成的node类有DefwithNode, TextNode, ExpressionNode, AssignmentNode, LineNode, BlockNode, ForNode, CodeNode, StatementNode, IfNode, ElseNode, ElifNode, DefNode, VarNode, SuiteNode。每个node类都定义有`emit()`用于生成对应的python代码。

## 将template转成python代码

[Template](https://github.com/webpy/webpy/blob/master/web/template.py#L846)在__init__()调用self.compile_template将template转成一个python函数的代码，再调用builtin方法compile()和exec()编译，当需要即执行新生成的函数。

将template转成python由[Template.generate_code](https://github.com/webpy/webpy/blob/master/web/template.py#L883)完成。这里略过Parse的细节。下面代码演示生成的python代码。
{% codeblock lang:python %}
import web

filename = 'templates/test.html'
code = web.template.Template.generate_code(open(filename, 'r').read(), filename)
print code
{% endcodeblock %}

以下为template test.html的内容，添加了一个if/else块:
{% codeblock lang:html %}
$def with (name)
Hello $name!

$if name == 'world':
    world again
$else:
    only hello
{% endcodeblock %}
生成的python代码：
{% codeblock lang:python %}
# coding: utf-8
def __template__ (name):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'Hello ', escape_(name, True), u'!\n'])
    extend_([u'\n'])
    if name == 'world':
        extend_([u'world again\n'])
    else:

        extend_([u'only hello\n'])

    return self
{% endcodeblock %}

## 编译python函数

生成代表python function的字符串后，还需要[compile()](https://github.com/webpy/webpy/blob/master/web/template.py#L912)和[exec()](https://github.com/webpy/webpy/blob/master/web/template.py#L803)才能生成可调用的对象。

在前边生成的代码，可以看到有创建外部类的对象，ForLoop(),TemplateResult()和escape_, 需要在comile时导入。
{% codeblock lang:python %}
import web

filename = 'templates/test.html'
code = web.template.Template.generate_code(open(filename, 'r').read(), filename)
#print code

# compile it
compiled_code = compile(code, filename, 'exec')
def escape(value, escape = True):
    if value is None:
        return ''
    return value

env = dict({},
           ForLoop= web.template.ForLoop,
           TemplateResult = web.template.TemplateResult,
           escape_ = escape)
exec(compiled_code, env)

t = env['__template__']
print t('world')
{% endcodeblock %}

生成的函数对象可以由env['__template__']获得。最后打印出的结果如下：
{% codeblock lang:html %}
Hello world!

world again

{% endcodeblock %}
