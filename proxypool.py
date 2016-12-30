# coding=utf-8

from multiprocessing import Queue, Process
from api.api_server import start_api_server
from spider.proxy_crawl import start_proxy_crawl
from validator.validator import validate_between_queue
from db.sql_helper import store_proxy


if __name__ == '__main__':
    # queue1为队列1，用来存放爬虫爬取到的尚未经过检验的代理（去重后）
    # 每个队列元素形式为：{'ip':ip, 'port':port}
    # queue2为队列2，用来存放成功经过检验后的代理
    # 每个队列元素为形式为:
    # {'ip':ip, 'port':port, 'level':level}
    q1 = Queue()
    q2 = Queue()

    p1 = Process(target=start_api_server)
    p2 = Process(target=start_proxy_crawl, args=(q1,))
    p3 = Process(target=validate_between_queue, args=(q1, q2))
    p4 = Process(target=store_proxy, args=(q2,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()