import requests
import json
import time
import random
import sys
import os
from tqdm import tqdm
from fake_useragent import UserAgent
# TODO: 正则化结果
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
timeout = (10, 30)
headers ={
    'User-Agent' : ua.random,
    'Referer' : 'https://www.bqg778.cc/',
    'Accept' : 'application/json, text/javascript, /; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie' : 'Hm_lvt_9c5f07b6ce20e3782eac91ed47d1421c=1769665977; HMACCOUNT=8B635B4223B07B07; siteurl=apibi.cc; Hm_lpvt_9c5f07b6ce20e3782eac91ed47d1421c=1769956460'
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

res_search = requests.get(url= url_search, params= params_search,headers= headers, timeout= timeout)
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

res_book = requests.get(url= url_book, params= params_book, headers= headers, timeout= timeout)
try:
    chapter = int(dict(json.loads(res_book.text))['lastchapterid'])
    print(f'一共有{chapter}章')
except Exception as e:
    print('章节还能错？')
    sys.exit(1)

time.sleep(2)

print('开始获取每章内容')
headers_ = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Cntrol": "no-cache",
    "Origin": "https://www.bqg778.cc",
    "Pragma": "no-cache",
    "Referer": "https://www.bqg778.cc/",
    "Sec-Ch-Ua": '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"
}
# 创建文件夹
os.makedirs(f'saved/{book_name}', exist_ok= True)

for i in tqdm(range(440,chapter + 1), desc= '下载进度', unit= '章'):


        params_chapter['chapterid'] = f'{i}'

        res_chaper = requests.get(url= url_chapter, params= params_chapter, timeout= timeout, headers= headers_)

        dict_res_chaper = dict(json.loads(res_chaper.text))

        text = dict_res_chaper['txt']
        chapter_name = dict_res_chaper['chaptername']

        with open(f'saved/{book_name}/{i}{chapter_name}.txt', 'w', encoding= 'utf-8') as f:
            f.write(text)


print('程序执行完毕')

