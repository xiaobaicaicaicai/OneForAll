import time
from bs4 import BeautifulSoup
from common.search import Search
from config.log import logger


class Gitee(Search):
    def __init__(self, domain):
        Search.__init__(self)
        self.source = 'GiteeSearch'
        self.module = 'Search'
        self.addr = 'https://search.gitee.com/'
        self.domain = domain
        self.header = self.get_header()

    def search(self, full_search=False):
        """
        向接口查询子域并做子域匹配
        """
        page_num = 1
        while True:
            time.sleep(self.delay)
            params = {'pageno': page_num, 'q': self.domain, 'type': 'code'}
            try:
                resp = self.get(self.addr, params=params)
            except Exception as e:
                logger.log('ERROR', e.args)
                break
            if not resp:
                break
            if resp.status_code != 200:
                logger.log('ERROR', f'{self.source} module query failed')
                break
            if 'class="empty-box"' in resp.text:
                break
            soup = BeautifulSoup(resp.text, 'html.parser')
            subdomains = self.match_subdomains(soup.text, fuzzy=False)
            if not subdomains:
                break
            if not full_search and subdomains.issubset(self.subdomains):
                # 在全搜索中发现搜索出的结果有完全重复的结果就停止搜索
                break
            self.subdomains = self.subdomains.union(subdomains)
            if '<li class="disabled"><a href="###">' in resp.text:
                break
            page_num += 1
            if page_num >= 100:
                break

    def run(self):
        """
        类执行入口
        """
        self.begin()
        self.search()
        self.finish()
        self.save_json()
        self.gen_result()
        self.save_db()


def run(domain):
    """
    类统一调用入口

    :param str domain: 域名
    """
    query = Gitee(domain)
    query.run()


if __name__ == '__main__':
    run('qq.com')
