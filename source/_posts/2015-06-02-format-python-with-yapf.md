---
layout: post
title: "format python with yapf"
description: ""
category: python
tags: [python, yapf]
---

Ref: https://github.com/google/yapf


## Install

    $ pip install yapf

## Usage

    yapf --style pip8.style main.py test.py


pip8.style

    [style]
    based_on_style = pep8
    spaces_before_comment = 4
    split_before_logical_operator = true


