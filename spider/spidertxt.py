import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# 目录页URL
base_url = 'https://sanguo.5000yan.com/baihuawen/'
catalog_url = base_url  # 假设目录页是基础URL

# 获取目录页内容
print("开始抓取目录页")
response = requests.get(catalog_url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有章节的<a>标签
chapter_links = []
for li in soup.find_all('li', class_='p-2'):
    a_tag = li.find('a', target='_blank')
    if a_tag:
        href = a_tag['href']
        title = a_tag.get_text()
        full_url = urljoin(base_url, href)
        chapter_links.append((full_url, title))

print(f"获取到 {len(chapter_links)} 个章节链接")

# 定义函数抓取单个章节内容
def get_chapter_content(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='grap')
        if content_div:
            content = content_div.get_text()
            return content
        else:
            return ''
    except Exception as e:
        print(f'Error fetching {url}: {e}')
        return ''

# 写入所有章节内容到txt文件
with open('sanguo.txt', 'w', encoding='utf-8') as f:
    for url, title in chapter_links:
        print(f"正在抓取章节: {title}")
        f.write(f'## {title}\n\n')
        content = get_chapter_content(url)
        f.write(content)
        f.write('\n\n')
        time.sleep(1)  # 延迟1秒，避免对服务器造成负担
    print("所有章节抓取完成")