from common.query import Query


class Ximcx(Query):
    def __init__(self, domain):
        Query.__init__(self)
        self.domain = domain
        self.module = 'Dataset'
        self.source = 'XimcxQuery'
        self.addr = 'http://sbd.ximcx.cn/DomainServlet'

    def query(self):
        """
        向接口查询子域并做子域匹配
        """
        self.header = self.get_header()
        self.proxy = self.get_proxy(self.source)
        data = {'domain': self.domain}
        resp = self.post(self.addr, data=data)
        if not resp:
            return
        json = resp.json()
        subdomains = self.match_subdomains(str(json))
        # 合并搜索子域名搜索结果
        self.subdomains = self.subdomains.union(subdomains)

    def run(self):
        """
        类执行入口
        """
        self.begin()
        self.query()
        self.finish()
        self.save_json()
        self.gen_result()
        self.save_db()


def run(domain):
    """
    类统一调用入口

    :param str domain: 域名
    """
    query = Ximcx(domain)
    query.run()


if __name__ == '__main__':
    run('example.com')
