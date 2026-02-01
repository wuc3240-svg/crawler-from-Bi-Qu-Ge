import requests
import json
import time
import random
import sys
import os
from tqdm import tqdm
from fake_useragent import UserAgent
# TODO：模块化
# TODO：日志
# TODO：错误重试
# TODO: 进度保存
# TODO：多书籍爬取,与搜索选取
# TODO：IP池和多线程

'''
思路
1. 搜索,获取id
2. 使用id,获取章节数
3.使用章节数进行循环爬取
'''

book_name = input('请输入书名：')
ua = UserAgent()

headers ={
    'User_Agent' : ua.random,
    'referer' : 'https://www.bqg778.cc/'
}
url_search = 'https://apibi.cc/api/search'
url_book = 'https://apibi.cc/api/book'
url_chapter = 'https://apibi.cc/api/chapter'

params_search = {
    'q' : book_name
}
params_book = {
    'id' : ''
}
params_chapter = {
    'id' : '',
    'chapterid' : ''
}



print('开始获取书籍id')

res_search = requests.get(url= url_search, params= params_search,headers= headers)
try:
    book_id = dict(json.loads(res_search.text))['data'][0]['id']
    print(f'书籍的id是:{book_id}')
except Exception as e:
    print('未找到该书籍')
    sys.exit(1)

params_book['id'] = f'{book_id}'
params_chapter['id'] = f'{book_id}'
time.sleep(2)

print('开始获取总章节数')

res_book = requests.get(url= url_book, params= params_book, headers= headers)
try:
    chapter = dict(json.loads(res_book.text))['lastchapterid']
    print(f'一共有{chapter}章')
except Exception as e:
    print('章节还能错？')
    sys.exit(1)

time.sleep(2)

print('开始获取每章内容')

# 创建文件夹
os.makedirs(f'saved/{book_name}', exist_ok= True)

for i in tqdm(range(1,chapter + 1), desc= '下载进度', unit= '章'):

    try:
        params_chapter['chapterid'] = f'{i}'

        res_chaper = requests.get(url= url_chapter, params= params_chapter)
        dict_res_chaper = dict(json.loads(res_chaper.text))

        text = dict_res_chaper['txt']
        chapter_name = dict_res_chaper['chaptername']

        with open(f'saved/{book_name}/{i}{chapter_name}.txt', 'w', encoding= 'utf-8') as f:
            f.write(text)
    except Exception as e:
        print(f'第{i}个章节获取失败')

    time.sleep(random.uniform(2,3))

print('程序执行完毕')
