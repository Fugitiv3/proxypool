# coding=utf-8

from gevent import monkey
monkey.patch_all()
import time
import gevent
from gevent.pool import Pool
from spider.html_parser import HTMLParser
from db.sql_helper import SqlHelper
from validator.validator import get_my_ip, validate_proxy_in_db
import config


class ProxyCrawl():
    '''代理爬虫'''
    # proxy_set为集合，它的作用是去重
    # 每个元素为字符串，形式为：'ip:port'
    proxy_set = set()

    def __init__(self, queue1):
        '''初始化

        queue1为队列1，存放的是直接爬取的还尚未经过验证的代理
        每个元素为字典形式: {'ip':ip, 'port':port}'''
        self.crawl_pool = Pool(config.THREAD_NUM)
        self.queue1 = queue1

    def crawl(self, parser):
        '''抓取代理（针对单个parser的所有url）

        parser为字典，参考config.PARSER_LIST中的元素

        无返回值'''
        htmlparser = HTMLParser()
        for url in parser['urls']:
            response = htmlparser.get_response(
                url=url, fuck_gfw=parser['fuck_gfw'])
            if response:
                proxy_list = htmlparser.parse(response, parser)
                if proxy_list:
                    for proxy in proxy_list:
                        proxy_str = '{}:{}'.format(proxy['ip'], proxy['port'])
                        # 利用proxy_set避免重复
                        # 去重后以{'ip':ip, 'port':port}字典形式放入queue1队列中
                        if proxy_str not in self.proxy_set:
                            self.proxy_set.add(proxy_str)
                            self.queue1.put(proxy)


    def run(self):
        '''定期清洗数据库，并且如果必要的话再进行爬虫抓取代理

        取出数据库中所有代理进行一次检测，根据检测结果更新数据库
        如果更新后数据库里总代理数小于指定的下限值，就会进行一次整个的爬虫抓取
        无论总代理数是否小于指定的下限值，之后都会休眠一段时间，等待下次的循环调用'''
        while True:
            print('begin......')
            self.proxy_set.clear()
            sqlhelper = SqlHelper()
            sqlhelper.init_db()
            proxy_tuple_list = sqlhelper.select()
            # 对数据库中的每个代理进行检测并更新数据库（更新or删除对应条目）
            my_ip = get_my_ip()
            spawns = []
            for proxy_tuple in proxy_tuple_list:
                proxy = {
                    'ip': proxy_tuple[0],
                    'port': proxy_tuple[1]
                }
                spawns.append(
                    gevent.spawn(
                        validate_proxy_in_db, proxy, my_ip, self.proxy_set))
            gevent.joinall(spawns)
            # 检测完所有的代理和更新数据库后，获取数据库中剩下所有总代理数
            db_proxy_num = len(self.proxy_set)
            msg = 'now there are {} proxies in the database'.format(
                db_proxy_num)
            # 如果db_proxy_num小于MIN_DB_PROXY_NUM就进行一次爬虫抓取
            if db_proxy_num < config.MIN_DB_PROXY_NUM:
                msg += '\r\nit is less than MIN_DB_PROXY_NUM: {}'.format(
                    config.MIN_DB_PROXY_NUM)
                msg += '\r\ncrawl starts......'
                print(msg)
                self.crawl_pool.map(self.crawl, config.PARSER_LIST)
                print('crawl ends, and no matter whether it meets the ' +
                    'requirement, wait for the next time to run')
            else:
                msg += '\r\nit meets the requirement, wait for the next time to run'
                print(msg)

            time.sleep(config.UPDATE_TIME)


def start_proxy_crawl(queue1):
    '''实例化ProxyCrawl并调用run方法

    queue1为队列1，存放的是直接爬取的还尚未经过验证的代理
    每个元素为字典形式: {'ip':ip, 'port':port}'''
    crawl = ProxyCrawl(queue1)
    crawl.run()