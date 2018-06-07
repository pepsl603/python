import requests
from bs4 import BeautifulSoup
import time
import re
import html

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
}

info_lists = []


def get_info(url):
    res_data = requests.get(url, headers=headers)
    if res_data.status_code == 200:
        # soup = BeautifulSoup(res_data.text, 'lxml')
        # title = re.findall('<h1>(.*?)</h1>', res_data.content.decode('utf-8'))
        contents = re.findall('<p>(.*?)</p>', res_data.content.decode('utf-8'), re.S)
        for content in contents:
            content = html.unescape(content)
            with open('./txt/斗破苍穹.txt', 'a+', encoding='utf-8') as f:
                f.write(content + '\n')
    else:
        print('获取失败:', url)


if __name__ == '__main__':
    print('start')
    urls = ['http://www.doupoxs.com/doupocangqiong/{}.html'.format(str(i)) for i in range(2, 1666)]
    with open('./txt/斗破苍穹.txt', 'w+', encoding='utf-8') as f:
        f.write('斗破苍穹' + '\n\n\n')
    for url in urls:
        # print(url)
        get_info(url)
        # time.sleep(1)
    print('end')
