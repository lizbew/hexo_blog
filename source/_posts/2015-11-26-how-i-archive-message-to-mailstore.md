---
layout: post
title: "从outlook导出邮件存储在MailStore"
description: "export message from outlook using python script, and import to MailStore"
category: tool
tags: [python, outlook, MailStore]
---


工作中每天都要收到大量的邮件，实在是太多了。 设置了定期归档任务， 将旧的邮件都移到了archive folder里，也有换时间来切换不同的文件， 来保持服务器上空间不会满，加快outlook启动的时间。但当要查找旧邮件时，就需要打开archive folder, 以致于Outlook卡死。一直想找个邮件归档软件来保存outlook里的旧邮件， 于是找到了MailStore。

MailStore功能是非常强大的，支持多种邮件导入方式，比如从IMAP、磁盘上的eml\msgy文件，也支持outlook。导入归档邮件最简单的方式就是读取outlook使用的pst文件，不过免费版本的Home Edition并不支持，需要Pro Edtion。归档邮件可以像在outlook两档式的查看，也支持用outlook来查看。

我所解决的问题就是，将归档的message从outlook导出来保存为.msg文件， 使用python 脚本来实现的。 在保存为.msg文件后，就可以导入到Mail Store里了。

看几张图吧。

* MailStore的主界面，最左侧是工具栏/导行，中间是邮件列，右边是邮件内容。 注意，邮件内容上的工具栏，可以从outlook时直接打开邮件，当想要回复旧的邮件时就非常之方便了。

![pic1](/images/post/MailStore-01.png)

* "Archive Email"选项。这里使用的Profile Name 是EML and MSG Files。从文件夹导入MSG 文件成功， MailStore会删除MSG文件。

![pic2](/images/post/MailStore-02.png)


下面是使用的python 脚本， 邮件文件存放到接收日期对应的子文件夹下。由于使用了outlook的COM接口， 在运行脚本的过程中， outlook会一直等待，这时是没法正常使用outlook的。所以，最好是在下班后启动脚本了。

{% codeblock lang:python %}
#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import win32com.client

def saveMailAsFile(mailItem):
    root_dir = r'D:\msgStore2'
    try:
        dest_dir = os.path.join(root_dir, mailItem.ReceivedTime.Format('%Y/%m/%d'))
    except:
        return
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    mailItem.SaveAs(os.path.join(dest_dir, str(mailItem.EntryID) + '.msg'))


def deleteMail(mailItem):
    try:
        mailItem.Delete()
    except Exception, e:
        print 'Exception when delete', mailItem.Subject
        print e


def saveMailAndDelete(mailItem):
    saveMailAsFile(mailItem)
    deleteMail(mailItem)

def openOutlookFolderWithConfig(config, mailHandler):
    outlookApp = win32com.client.gencache.EnsureDispatch('Outlook.Application')
    nsMAPI = outlookApp.GetNamespace('MAPI')
    folder = nsMAPI

    fPaths = config['folder'].strip('/').split('/')
    for p in fPaths:
        folder = folder.Folders.Item(p)
    print 'Location:', folder.FullFolderPath
    
    while True:
        emailList = folder.Items
        print len(emailList)
        if len(emailList) == 0:
            break
        for msg in emailList:
            mailHandler(msg)
            
def exportMSG():
    config = {
        'folder': 'Archive Folders/Inbox',
    }
    openOutlookFolderWithConfig(config, saveMailAndDelete)

if __name__ == '__main__':
    exportMSG()
{% endcodeblock %}

* 总有那么一些邮件是没办法导入的。我是直接忽略了。

![pic3](/images/post/MailStore-03.png)


