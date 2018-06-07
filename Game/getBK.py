import requests
from bs4 import BeautifulSoup
import time


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
}

info_lists = []


def get_info(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    users = soup.select('div.author.clearfix > a > h2')
    contents = soup.select('a.contentHerf > div > span')
    nums = soup.select('div.stats > span.stats-vote > i')
    ids = soup.select('a.contentHerf')
    for user, content, num, id in zip(users, contents, nums, ids):
        data = {
            'name': user.get_text().strip(),
            'zan': num.get_text().strip(),
            'content': content.get_text().strip(),
            'id': id.get('href').split('/')[2]
        }
        # print(data)
        info_lists.append(data)


if __name__ == '__main__':
    urls = ['https://www.qiushibaike.com/text/page/{}/'.format(str(i)) for i in range(1, 13)]
    for url in urls:
        print(url)
        get_info(url)
        time.sleep(1)
    print('写文件')
    for info in info_lists:
        with open('./txt/qiushi.txt', 'a+', encoding='utf-8') as f:
            f.write(info['id'] + '###' + info['name'] + '\n')
            f.write(info['content'] + '\n\n')
    print('结束')
