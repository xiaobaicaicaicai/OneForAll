from common.query import Query


class ThreatMiner(Query):
    def __init__(self, domain):
        Query.__init__(self)
        self.domain = domain
        self.module = 'Intelligence'
        self.source = 'ThreatMinerQuery'
        self.addr = 'https://www.threatminer.org/getData.php'

    def query(self):
        """
        向接口查询子域并做子域匹配
        """
        self.header = self.get_header()
        self.proxy = self.get_proxy(self.source)
        params = {'e': 'subdomains_container',
                  'q': self.domain, 't': 0, 'rt': 10}
        resp = self.get(self.addr, params)
        if not resp:
            return
        subdomains = self.match_subdomains(resp.text)
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
    query = ThreatMiner(domain)
    query.run()


if __name__ == '__main__':
    run('example.com')
