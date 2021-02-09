from mysql import Mysql
from urllib import request
import urllib

def getAll():
    url = 'https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=%E6%9D%8E%E5%B0%8F%E5%86%89'
    response = request.urlopen(url)
    page = response.read()
    page = bytes.decode(page)
    content = eval(page)
    print(content)
if __name__ == '__main__':
    getAll()