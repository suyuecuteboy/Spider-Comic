import requests
from urllib.request import urlretrieve
from urllib.parse import urlparse
import re
#导入需要的库和包


class Spider():
#创建一个类



    HEADERS = {
        'User-Agent': '自定义User-Agent',
        'referer': 'https://www.pangci.cc/works/27192/'
    }
# 定义类的实例



    def __init__(self, url):
        self.url = url
        self.links = set()
        parse_url = urlparse(url)
        self.base_url = '{}://{}'.format(parse_url[0], parse_url[1])    
# 初始化工作



    def start(self):
        self._extract_links()
        self._upload_img() 
# 启动爬虫



    def _extract_links(self):
        rsp = requests.get(self.url, headers=Spider.HEADERS)
        if rsp.status_code == 200:
            html = rsp.text
            links = re.findall(r'<div class="p"><a href="(.*?)" target="_blank"><img src="https', html)
            for link in links:
                self.links.add('{}{}'.format(self.base_url, link))
#获取url


    def _extract_data(self, url):
        rsp = requests.get(url, headers=Spider.HEADERS)
        if rsp.status_code == 200:
            html = rsp.text
            links = re.findall(
                r'<li style="margin-top:0px;"><a class="piclink" href=".*?" target="_blank"><img src="(.*?)" alt="(.*?)" ',
                html)
            for link in links:
                img_url = link[0]
                img_name = link[1]
                filename = r'胖次网图片/{}.jpg'.format(img_name)
                urlretrieve(img_url, filename)
#获取图片并上传


    def _upload_img(self):
        for url in self.links:
            self._extract_data(url)
#批量上传图片


if __name__ == '__main__':
    spider = Spider('https://www.pangci.cc/user/3749/works.html')
    spider.start()
