# 网络爬虫项目

这是一个基于Python的简单网络爬虫项目，用于从百度新闻搜索中爬取与指定关键词相关的新闻标题和链接，并对新闻内容进行评分。该项目还支持将爬取的结果存储到MySQL数据库中。

## 功能描述

- 输入关键词进行新闻搜索
- 爬取搜索结果中的新闻标题和链接
- 根据新闻内容和标题中的关键字进行评分
- 将爬取结果显示在图形界面中
- 将爬取结果存储到MySQL数据库中

## 项目结构

```
.
├── main.py         # 主程序文件
├── README.md       # 项目说明文件
├── requirements.txt# 依赖项文件
└── crawler.log     # 日志文件
```

## 依赖项

该项目依赖以下Python库：

- tkinter
- requests
- re
- pymysql
- logging

## 使用方法

1. 在程序界面的输入框中输入关键词。
2. 点击“开始爬取”按钮开始爬取与关键词相关的新闻。
3. 爬取完成后，会弹出一个新窗口显示爬取结果及评分。
4. 点击“存入数据库”按钮将结果存入MySQL数据库。

## 数据库配置

在运行程序之前，请确保已在本地安装MySQL数据库，并根据需要创建数据库和表。程序中使用的数据库连接配置如下：

```python
def connect_to_database():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="你的数据库密码",
        database="你的数据库名称"
    )
```

## 日志记录

程序运行过程中会生成一个`crawler.log`文件，记录爬取过程中的重要信息和错误，便于日后排查问题。