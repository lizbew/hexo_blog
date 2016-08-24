---
layout: post
title: "Note for build blog with jekyll"
description: "memo for jekyll commands"
category: site
tags: [jekyll]
---

Content of this blog is base on [Jekyll Quick Start](http://jekyllbootstrap.com/usage/jekyll-quick-start.html)

Run Locally
-----------

- First all, need to install tool `jekyll`

{% codeblock lang:console %}
    $ get install jekyll
{% endcodeblock %}

- After pull jekyll code and configured, then can start a local server. Open http://localhost:4000/ to access it.

{% codeblock lang:console %}
    $ cd USERNAME.github.com
    $ jekyll --server
{% endcodeblock %}


Create content
---------------
- Create a post. New file is created under folder `./_post`

{% codeblock lang:console %}
    $ rake post title="Hello World"
{% endcodeblock %}

- Create a page

{% codeblock lang:console %}
    $ rake page name="about.md"
    $ rake page name="pages/about.md"
    $ rake page name="pages/about"    # will create file ./pages/about/index.html
{% endcodeblock %}

Publish
-------

- Commit blog change to github

{% codeblock lang:console %}
    $ git add .
    $ git commit -m "a new blog"
    $ git push origin master
{% endcodeblock %}



