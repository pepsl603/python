import re
import urllib
import urllib3
import requests
import random


def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    html = html.decode('utf-8')
    return html


def getImgSafe(url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
        "Host": "img2.imgtn.bdimg.com",
        "Referer": "http://img2.imgtn.bdimg.com/it/u=3588772980,2454248748&fm=27&gp=0.jpg"}

    req = urllib.request.Request(url, headers=headers)
    x = urllib.request.urlopen(req)
    sourceCode = x.read()


    html = sourceCode.decode('utf-8')
    print(html)


def getImage(html):
    reg = r'"thumbURL":"(.*?\.jpg)",'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    # return imglist
    # print(imglist)
    # for imgurl in imglist:
    #     urllib.request.urlretrieve(imgurl, '\image\1.jpg')
    url = imglist[0]
    print(url)
    getImgSafe(url)
    # urldata = requests.get(url)
    # print(urldata)


html = getHtml('http://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm='
               '-1&cl=2&ie=gb18030&word=%CD%BC%C6%AC&fr=ala&ala=1&alatpl=others&pos=0')
# print(html)
getImage(html)


