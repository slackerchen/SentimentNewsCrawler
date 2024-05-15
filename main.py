from tkinter import *
from tkinter.messagebox import showinfo
import requests
import re
import pymysql
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, filename='crawler.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 显示爬取结果的函数
def display_results():
    top = Toplevel()
    top.title("爬取结果")
    top.geometry("1000x400")

    scrollbar = Scrollbar(top)
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(top, yscrollcommand=scrollbar.set)
    listbox.pack(fill=BOTH, expand=1)

    for i in range(len(title)):
        listbox.insert(END, f"{i+1}. {title[i]} - {href[i]} - 评分: {scores[i]}")

    scrollbar.config(command=listbox.yview)

# 爬虫函数
def crawler():
    try:
        global company, title, href, scores
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        company = E1.get()
        url = 'http://www.baidu.com/s?tn=news&rtt=1&wd=' + company
        res = requests.get(url, headers=headers).text
        p_href = '<h3 class="news-title_1YtI1 "><a href="(.*?)"'
        href = re.findall(p_href, res, re.S)
        p_title = '<h3 class="news-title_1YtI1 ">.*?>(.*?)</a>'
        title = re.findall(p_title, res, re.S)
        for i in range(len(title)):
            title[i] = re.sub('<.*?>', '', title[i].strip())
        scores = score_articles(headers)
        showinfo("结果", f"{company}爬虫成功！")
        logging.info(f"{company}爬虫成功")
        display_results()  # 显示结果
    except Exception as e:
        logging.error(f"{company}爬虫失败: {e}")
        showinfo("结果", f"{company}爬虫失败！")

# 评分函数
def score_articles(headers):
    score = []
    keywords = {
        '违约': 20,
        '不合格': 15,
        '偷税': 10,
        '丑闻': 25,
        '失信': 20,
        '欺诈': 15,
        '违法': 10,
        '涉嫌犯罪': 30,
        '涨': 20,
        '下滑': 30,
        'AI': 40
    }
    for i in range(len(title)):
        num = 100  # 初始化评分为100
        try:
            article = requests.get(href[i], headers=headers, timeout=10).text
            for k, v in keywords.items():
                if k in article or k in title[i]:
                    num -= v  # 根据关键词扣分
        except Exception as e:
            logging.error(f"爬取文章失败: {href[i]} - {e}")
            num -= 50  # 如果文章爬取失败，扣除50分
        score.append(num)
    return score

# 保存到数据库的函数
def save():
    try:
        conn = connect_to_database()
        create_result_table(conn)
        insert_results(conn)
        conn.close()
        showinfo("存储", "存入数据库成功")
        logging.info("存入数据库成功")
    except Exception as e:
        logging.error(f"存入数据库失败: {e}")
        showinfo("存储", "存入数据库失败")

# 连接数据库
def connect_to_database():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="sentiment_analysis"
    )

# 创建结果表
def create_result_table(connection):
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS result')
    sql = """
        CREATE TABLE result (
            company CHAR(20),
            title CHAR(100),
            href VARCHAR(255),  -- 增加href列的长度
            score INT
        )
    """
    cursor.execute(sql)
    logging.info("成功创建结果表")

# 插入结果
def insert_results(connection):
    cursor = connection.cursor()
    for i in range(len(title)):
        sql = 'INSERT INTO result(company, title, href, score) VALUES (%s, %s, %s, %s)'
        cursor.execute(sql, (company, title[i], href[i], scores[i]))
    connection.commit()

# 主窗口设置
root = Tk()
root.title("网络爬虫")
root.geometry("300x200")

# 标签和输入框
L1 = Label(root, text="关键词：", font=20)
L1.place(x=10, y=20)
E1 = Entry(root, bd=5, font=20, width=15)
E1.place(x=80, y=20)

# 按钮
B1 = Button(root, text="开始爬取", font=20, width=10, command=crawler)
B1.place(x=10, y=80)
B2 = Button(root, text="存入数据库", font=20, width=10, command=save)
B2.place(x=130, y=80)

root.mainloop()
