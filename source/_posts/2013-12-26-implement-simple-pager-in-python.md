---
layout: post
title: "用Python实现简单的分页功能"
description: ""
category: python
tags: [python, pager]
---

原始发布于： http://blog.viifly.com/blog/posts/5798429187899392

直接上代码 

{% codeblock lang:python %}
    class Pager(object):
        win_size = 4
        def __init__(self, total, page_no=1, page_size=15):
            self.total_records = total
            self.total_page = self.get_page_count(total, page_size)
            self.page_size = page_size
            self.page_no = 1 if page_no < 1 else min(page_no, self.total_page)
            page_win_no = self.get_page_count(self.page_no, self.win_size)
            self.page_win = range((page_win_no-1)*self.win_size +1, min(self.total_page, page_win_no * self.win_size)+1)
            self.record_range = ((self.page_no-1)*self.page_size + 1, min(self.total_records, self.page_no*self.page_size))

        def get_page_count(self, total, page_size):
            return total/page_size + (1 if total % page_size > 0 else 0)
{% endcodeblock %}

使用时，只需传递记录总数和当前页数，如`pager = Pager(100,2)`。

下面是使用Jinja2时template代码：

{% raw %}
    {% if pager %}
    <div>
      {% if pager.page_no > 1 %}<a href="?page={{ pager.page_no-1 }}">Previous</a>{% endif %}
      {% for p in pager.page_win %} 
      {% if p == pager.page_no %}
      <span>{{ p }}</span>
      {% else %}
      <a href="?page={{ p }}">{{ p }}</a>
      {% endif %}
      {% endfor %}
      ({{ pager.record_range[0] }}-{{ pager.record_range[1] }}/{{ pager.total_records }})
      {% if pager.page_no < pager.total_page %}<a href="?page={{ pager.page_no + 1}}">Next</a>{% endif %}
    </div>
    {% endif %}
{% endraw %}  

效果如下：

![简单分页](/images/post/pager.png)


