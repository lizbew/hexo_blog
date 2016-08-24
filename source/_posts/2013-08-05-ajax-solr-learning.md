---
layout: post
title: "Learning Ajax-solr"
description: "AJAX Solr is a JavaScript library for creating user interfaces to Apache Solr"
category: "Web"
tags: [solr, js, ajaxsolr]
---

[ajax-solr](https://github.com/evolvingweb/ajax-solr)在github主面的介绍是 

> AJAX Solr is a JavaScript library for creating user interfaces to Apache Solr.

从字面上理解就是AJAX Solr是用于创建Apache Solr界面的javascript库。它确实是用来创建web UF的库，因为javascript里访问json数据是非常直接的，而不需要像Java客户端库那样将URI封装成object来访问。AJAX Solr统一管理了对json URI的访问，及页面各个部分对返回结果的响应。

##主要的类##

ajax-solr中提供了如下几个基本的类，所有类都包含在namesapce `AjaxSolr`中。其中`Manager`是最主要类的，每个ajax solr应用都需要一个`Manager`的实例。

- AjaxSolr.AbstractManager, AjaxSolr.Manager  ->主要controller类，包含有AbstractWidget的列表和一个ParameterStore 
- AjaxSolr.AbstractWidget -> 页面widget抽象类
- AjaxSolr.Parameter -> 代码URL中参数
- AjaxSolr.ParameterStore -> 保存所有用到的参数

##页面的初始化##

页面的初始化通常是在`document.ready()`中完成，或是借助jquery库的`$(function(){...})`。

首先需要初始化一个`Manager`初始，再创建一些Widget并通过方法`Manager.addWidget`添加到Manager中，最后再调用`Manager.init()`。`Manager.init()`会调用每一个Widget的`init()`。

{% codeblock %}
  solrUrl: 'http://localhost:8983/solr/'
});

Manager.addWidget(new AjaxSolr.SearchCriteriaWidget({
  id: "searchCriteria",
  target: '#qform'
}));
Manager.init();
{% endcodeblock %}

##Manager.doRequest##

所有向solr 发出的请求都是通过`Manager.doRequest()`。由于本人UML知识有限也画不了漂亮的图，用visio尝试了一次还是改用如下文本形式来表示方法调用关系了。 首先检查是否需要init(),设置好ParameterStore里的参数，再对调用每一个widget的`beforeRequest()`，然后调用具体Manager实现类的`executeRequest()`。`executeRequest()`会真正向solr sever发出请求，获得server返回的JSON 数据；如果成功，则调用每一个widget的`afterRequest()`，失败调用`errorHandler()`。

<pre>
Manager.doRequest()
 - .init()
 - .store.save()
 - each-widgets.beforeRequest()
 - .executeRequest()
 - - .handleResponse() if done
 - - - each-widgets.afterRequest()
 - - .errorHandler() if error
</pre>


{% codeblock %}
Manager.doRequest();
{% endcodeblock %}

search时`q`所用到的用到的内容与格式，还是需要自己组装起来。


##实现Widget##

将页面实现为不同的Widget，所得到的优势就是可以将json response写在不同的Widget里，便于化开不同的功能和管理。

如下创建一个`SearchCriteriaWidget`，保存到文件SearchCriteriaWidget.js。

{% codeblock %}
  if (typeof define === 'function' &amp;&amp; define.amd) {
    define(['core/AbstractWidget'], callback);
  }
  else {
    callback();
  }
}(function () {

(function ($) {

AjaxSolr.SearchCriteriaWidget = AjaxSolr.AbstractWidget.extend({
	//Widget implementation here

});

})(jQuery);

}));
{% endcodeblock %}

##结论##

ajax-solr在对solr json的了解上并不能给你带来多大的帮助，但可以简化UI的实现。ajax-solr所采用的Manager/Widget模式，给了我在实现ajax 应用上一些启发。
