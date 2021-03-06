import re
import csv
import time
import json
import requests
from requests.exceptions import RequestException


# 抓取单页
def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.87 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


# 正则提取
def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?'
        'releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
        re.S
    )
    items = re.findall(pattern, html)
    # print(items)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()
        }


# 写入txt文件
def write_to_txtFile(content):
    with open('MovieTop100.txt', 'a', encoding='utf-8') as f:
        # print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


# 写入CSV文件表头
def write_to_csvField(filename):
    with open("MovieTop100.csv", 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, filename)
        writer.writeheader()


# 写入CSV文件内容
def write_to_csvRows(content, filename):
    with open("MovieTop100.csv", 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, filename)
        # writer.writeheader()    # 在抓取多页面时会造成表头重复
        writer.writerows(content)


def main(offset, fieldnames):
    url = 'http://maoyan.com/board/4?offset={0}'.format(offset)
    html = get_one_page(url)
    rows = []
    for item in parse_one_page(html):
        # print(item)
        # write_to_txtFile(item)
        rows.append(item)
    write_to_csvRows(rows, fieldnames)


if __name__ == "__main__":
    fieldnames = ["index", "image", "title", "actor", "time", "score"]
    write_to_csvField(fieldnames)
    for i in range(10):
        main(offset=i * 10, fieldnames=fieldnames)
        time.sleep(1)
