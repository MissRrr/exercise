'''
Created on Nov 25, 2020

@author: Celia
'''

import requests
from bs4 import BeautifulSoup
import bs4

def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        #判断返回的Response类型状态是否正常，否则抛出异常
        r.raise_for_status()
        #获取页面编码
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'occurred the exception'
      
      
def fill_news_list(news_list, html_doc):
    if html_doc == 'occurred the exception':
      return
    soup = BeautifulSoup(html_doc)
    a_lists=[]
    #找class是baijia-focus-list的div标签的子节点(通过tag的 .children 生成器,可以对tag的子节点进行循环)
    for ul in soup.find('div',attrs={'class':'baijia-focus-list'}).children:
        if isinstance(ul, bs4.element.Tag):
            #获取ul标签下的每一个li标签,ul('li')返回的是一个list
            li_lists = ul('li')
            #获取li标签下的a标签放进列表，这里li的类型是tag
            for li in li_lists:
              #li('a')返回的是一个list
              a_lists.append(li('a'))
    #a_list的元素是列表，元素里的列表放置的是一个Tag对象
    for i in range(len(a_lists)):
      news_list.append([a_lists[i][0].string.strip(),a_lists[i][0]['href'].strip()])
      
      
def print_news_list(ulist):
    if len(ulist)== 0:
      return
    for i in range(len(ulist)):
        u = ulist[i]
        print(f'{i+1}.\n新闻题目:"{u[0]}"\n新闻网页地址:{u[1]}')


if __name__ == '__main__':
  html_doc = getHTMLText('http://news.baidu.com')
  news_list = []
  fill_news_list(news_list,html_doc)
  print_news_list(news_list)
  
 
