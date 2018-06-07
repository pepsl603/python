import requests
from bs4 import BeautifulSoup
import time
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
}


very_url = 'http://bj.xiaozhu.com/limitaccess.php?limitaccess=%s'


def get_code(soup_text):
    print(soup_text)
    rs = r'limitaccess=(veryfy_\w*?)\''
    very_code = re.findall(rs, soup_text)
    if len(very_code) > 0:
        v_url = very_url % very_code[0]
        v_data = requests.get(v_url, headers=headers)
        v_soup = BeautifulSoup(v_data.text, 'lxml')
        print(v_soup)


def get_info(link_url):
    try:
        link_data = requests.get(link_url, headers=headers)
        link_soup = BeautifulSoup(link_data.text, 'lxml')
    except Exception as ex:
        print(ex)
    titles = link_soup.select('div.pho_info > h4 > em')
    prices = link_soup.select('#pricePart > div.day_l > span')
    addresses = link_soup.select('div.wrap.clearfix.con_bg > div.con_l > div.pho_info > p > span')
    names = link_soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')

    for title, address, price, name in zip(titles, addresses, prices, names):
        data = {
            '标题': title.get_text().strip(),
            '地址': address.get_text().strip(),
            '价格': price.get_text(),
            '业主': name.get('title')
        }
        print(data)


def get_link(url):
    try:
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        if soup.text.find('您访问过于频繁') >= 0:
            print('需要启用验证码', soup.decode_contents())
            get_code(soup.decode_contents())
            return ''
        links = soup.select('#page_list > ul > li > a')
    except Exception as ex:
        print(ex)
    for link in links:
        href = link.get('href')
        # print(href)
        get_info(href)
        time.sleep(1)


if __name__ == '__main__':
    urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(number) for number in range(1, 3)]
    for url in urls:
        # print(url)
        get_link(url)
        time.sleep(2)
