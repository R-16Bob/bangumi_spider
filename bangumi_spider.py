import requests
from bs4 import BeautifulSoup
import time
import csv

# 从Chrome浏览器复制User-Agent，将其伪装成浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
                 ' like Gecko) Chrome/88.0.4324.190 Safari/537.36'
}

url = "https://bgm.tv/anime/browser?sort=rank"

ls = []


def get_info(url):
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text.encode('utf-8'), 'lxml')
    # 使用beautifulsoup解析代码,注意第一个参数的.text
    titles = soup.select('div.inner > h3 > a')
    ranks = soup.select('div.inner > span.rank ')
    infos = soup.select('div.inner > p.tip')
    for title, rank, info in zip(titles, ranks, infos):
        data = {
            'rank':rank.get_text(),
            'title':title.get_text(),
            'ep':info.get_text().split('/')[0].strip(),
            'time':info.get_text().split('/')[1].strip(),
            'staff':info.get_text().split('/')[2:]
        }
        #print(data)
        ls.append(data)

if __name__ == '__main__':
    get_info(url)
    for i in range(2, 6):
        get_info(url+'&page={}'.format(i))
        time.sleep(1)



with open('bangumi_top.csv', 'w', newline='',encoding='utf-8-sig')as f:  #在当前路径下，以写的方式打开一个文件，如不存在则创建
    writer = csv.writer(f)
    writer.writerow(['rank', 'title', 'time', 'ep', 'staff'])
    for anima in ls:
        row = [anima['rank'], anima['title'],anima['time'],anima['ep']]
        staff = "/".join(anima['staff'])
        row.append(staff)
        print(staff)
        writer.writerow(row)
