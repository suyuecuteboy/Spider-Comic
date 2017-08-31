import requests
from urllib.request import urlretrieve
from urllib.parse import urlparse
import re


class Spider():
    HEADERS = {
        'User-Agent': '自定义 User-Agent',
        'referer': 'https://www.pangci.cc/works/27192/'
    }

    def __init__(self, url='https://www.pangci.cc/works/index_1.html', page=1):
        self.url = url
        self.page = page
        self.urls = []
        self.links = set()
        parse_url = urlparse(url)
        self.base_url = '{}://{}'.format(parse_url[0], parse_url[1])

    def start(self):
        self._obtain_urls()
        self._extract_links()
        self._extract_data()

    def _obtain_urls(self):
        for i in range(1, self.page + 1):
            self.urls.append(self.url.replace('index_1.html', 'index_{}.html'.format(i)))

    def _extract_links(self):
        for url in self.urls:
            rsp = requests.get(url, headers=Spider.HEADERS)
            if rsp.status_code == 200:
                html = rsp.text
                links = re.findall(r'<div class="p"><a href="(.*?)" target="_blank"><img src="https', html)
                for link in links:
                    self.links.add('{}{}'.format(self.base_url, link))

    def _extract_data(self):
        for url in self.links:
            rsp = requests.get(url, headers=Spider.HEADERS)
            if rsp.status_code == 200:
                html = rsp.text
                links = re.findall(
                    r'<li style="margin-top:0px;"><a class="piclink" href=".*?" target="_blank"><img src="(.*?)" alt="(.*?)" ',
                    html)
                for link in links:
                    img_url = link[0]
                    img_name = link[1]
                    print('正在下载{}'.format(img_name))
                    filename = r'二次元/{}.jpg'.format(img_name)
                    urlretrieve(img_url, filename)


if __name__ == '__main__':
    spider = Spider()
    spider.start()
