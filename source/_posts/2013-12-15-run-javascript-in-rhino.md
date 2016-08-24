---
layout: post
title: "通过Rhino在Java中执行Javascript程序"
description: ""
category: java
tags: [rhino, java, javascript]
---

原始发布于： http://blog.viifly.com/blog/posts/5890100969865216

最近尝试了在Java中执行Javascript程序。起因是要写一个FTP下文件和监视程序，嫌写配置文件太复杂，就考虑把配置文件写在javascript里（代码即配置），最终实现时的基本功能都是写在javascript里了，代码量要比java少得多。

要在java里调用javascript,就不得不提[Rhino][1]了。我实现时使用的包`javax.script.ScriptEngine`([docs][2])底层也是封装的Rhino。


先看下从[wikipedia][3]来的代码片段：

{% codeblock lang:java %}
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
    
public class RhinoEngine {
    public static void main(String[] args) {
        ScriptEngineManager mgr = new ScriptEngineManager();
        ScriptEngine engine = mgr.getEngineByName("JavaScript");
       
        try {
            engine.put("name", args[0]);
            engine.eval("print('Hello ' + name + '!')");
        } catch (ScriptException ex) {
            ex.printStackTrace();
        }    
    }
}
{% endcodeblock %}

Rhino执行的javascript代码可以直接用调用java的类。当然，使用到的类需要先import。引入单个类用`importClass(java.lang.String)`，而引用整个包用`importPackage(java.lang)`.然后就可以在javascript中新建实例了`var reader = new BufferedReader( new InputStreamReader(System['in']) )`.

Oracle的文档有更多[示例][4]。

  [1]: https://developer.mozilla.org/en-US/docs/Rhino
  [2]: http://docs.oracle.com/javase/7/docs/api/index.html?javax/script/ScriptEngine.html
  [3]: http://en.wikipedia.org/wiki/Rhino_%28JavaScript_engine%29
  [4]: http://docs.oracle.com/javase/7/docs/technotes/guides/scripting/programmer_guide/

