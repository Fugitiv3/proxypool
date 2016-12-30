# coding=utf-8

'''
配置选项
'''

import random
import os


# API服务端口
API_PORT = 8000

# ua
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

# 使用随机ua的header
HEADER = {
    'User-Agent': random.choice(USER_AGENTS)
}

# 请求超时时间(s)
TIMEOUT = 5

# ProxyCrawl.run调用的时间间隔(s)
UPDATE_TIME = 10 * 60

# 线程数（爬虫池大小）
THREAD_NUM = 10

# 解析列表（用于爬虫抓取代理时解析页面）
# - urls: 要抓取的目标页面
# - type: 提取方式（RegExp or XPath or Customized?）
# - pattern: 匹配模式
# - sub_pattern: 进一步提取ip,port,protocol的匹配模式
# - time_interval: 请求访问间隔(s)（反爬虫）
# - fuck_gfw: 是否用ss翻墙访问（有些提供代理的网站在墙外）
PARSER_LIST = [
    {
        'urls': ['http://www.xicidaili.com/{}/{}'.format(m, n) for m in ['nn', 'nt'] for n in range(1,8)],
        'type': 'xpath',
        'pattern': './/*[@id="ip_list"]/tr[position()>1]',
        'sub_pattern': {'ip':'./td[2]', 'port':'./td[3]'},
        'time_interval': 0,
        'fuck_gfw': False,
    },
    {
        'urls': ['http://www.ip181.com/daili/{}.html'.format(m) for m in range(1,8)],
        'type': 'xpath',
        'pattern': './/tbody/tr[position()>1]',
        'sub_pattern': {'ip':'./td[1]', 'port':'./td[2]'},
        'time_interval': 0,
        'fuck_gfw': False,
    },
    {
        'urls': ['http://www.cz88.net/proxy/{}'.format(m) for m in (['index.shtml']+['http_{}.shtml'.format(n) for n in range(2,11)])],
        'type': 'xpath',
        'pattern': './/*[@id="boxright"]//li[position()>1]',
        'sub_pattern': {'ip':'./div[1]', 'port':'./div[2]'},
        'time_interval': 0,
        'fuck_gfw': False,
    },
    {
        'urls': ['http://www.kuaidaili.com/free/{}/{}/'.format(m, n) for m in ['inha', 'intr', 'outha', 'outtr'] for n in range(1,8)],
        'type': 'xpath',
        'pattern': './/tbody/tr',
        'sub_pattern': {'ip':'./td[1]', 'port':'./td[2]'},
        'time_interval': 1,
        'fuck_gfw': False,
    },
    {
        'urls': ['http://incloak.com/proxy-list/?type=hs{}#list'.format(m) for m in (['']+['&start={}'.format(64*n) for n in range(1,9)])],
        'type': 'xpath',
        'pattern': './/tbody/tr',
        'sub_pattern': {'ip':'./td[1]', 'port':'./td[2]'},
        'time_interval': 0,
        'fuck_gfw': True,
    },
    {
        'urls': ['http://www.mimiip.com/{}/{}'.format(m,n) for m in ['gngao','gnpu','gntou','hw'] for n in range(1,8)],
        'type': 'xpath',
        'pattern': './/table[@class="list"]/tr[position()>1]',
        'sub_pattern': {'ip':'./td[1]', 'port':'./td[2]'},
        'time_interval': 0,
        'fuck_gfw': False,
    },
    {
        'urls': ['http://cn-proxy.com/','http://cn-proxy.com/archives/218'],
        'type': 'xpath',
        'pattern': './/table[@class="sortable"]/tbody/tr',
        'sub_pattern': {'ip':'./td[1]', 'port':'./td[2]'},
        'time_interval': 0,
        'fuck_gfw': True,
    },
    {
        'urls': ['http://www.66ip.cn/{}.html'.format(m) for m in range(1,8)],
        'type': 'xpath',
        'pattern': './/div[@id="main"]//table/tr[position()>1]',
        'sub_pattern': {'ip':'./td[1]', 'port':'./td[2]'},
        'time_interval': 0,
        'fuck_gfw': False,
    },
    {
        'urls': ['http://www.66ip.cn/areaindex_35/{}.html'.format(m) for m in range(1,8)],
        'type': 'xpath',
        'pattern': './/div[@id="main"]//table/tr[position()>1]',
        'sub_pattern': {'ip':'./td[1]', 'port':'./td[2]'},
        'time_interval': 0,
        'fuck_gfw': False,
    },
    {
        'urls': ['https://proxy-list.org/english/index.php?p={}'.format(m) for m in range(1,11)],
        'type': 'customized',
        'function_name': 'proxylist_parser',
        'pattern': './/*[@id="proxy-table"]//script',
        'time_interval': 0,
        'fuck_gfw': False,
    }
]

# shadowsocks本地代理（翻墙时需要）
SS_PROXIES = {
    'http': 'http://127.0.0.1:1080',
    'https': 'http://127.0.0.1:1080'
}

# 数据库连接配置
DB_CONFIG = {
    'CONNECT_STRING': 'sqlite:///' + os.path.dirname(__file__) + '/proxies.db',
    'CONNECT_ARGS': {
        'check_same_thread': False
    }
}

# 允许的数据库中所有代理总数的最小值
# (一般爬取到的匿名代理和透明代理会各占一半)
MIN_DB_PROXY_NUM = 60