import requests
from bs4 import BeautifulSoup
import urllib

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
}

url = 'https://list.jd.com/list.html?cat=9987,653,655'
url = 'http://bj.xiaozhu.com/'

res = requests.get(url, headers=headers, verify=True)

# urllib.request.urlretrieve('http://img11.360buyimg.com/n7/jfs/t3466/216/1440570101/297093/187de6d4/5825d2e7N5349a01a.jpg', './image/1.jpg')

try:
    # print(res.url)
    # print(res.text)
    soup = BeautifulSoup(res.text, 'html.parser')
    # soup = BeautifulSoup(res.text, 'html5lib')
    # print(soup.prettify())

    # print(soup)
    # plist > ul > li:nth-child(1) > div > div.p-img > a > img

    # images = soup.select('#plist > ul > li > div > div.p-img > a > img')
    # pic_nums = 1
    # for img in images:
    #     # print(img)
    #     src = img.get('src')
    #     if not src:
    #         src = img.get('data-lazy-img')
    #     # print(src)
    #     pic_url = 'http:%s' % src
    #     print(pic_url)
    #     urllib.request.urlretrieve(pic_url, './image/%s.jpg' % pic_nums)
    #     pic_nums += 1

    prices = soup.select('#page_list > ul > li > div.result_btm_con.lodgeunitname > span.result_price > i')
    for price in prices:
        print(price.get_text())



except ConnectionError:
    print('拒绝连接')


