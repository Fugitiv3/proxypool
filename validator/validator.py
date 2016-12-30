# coding=utf-8

from gevent import monkey
monkey.patch_all()
import re
from multiprocessing import Process
import gevent
import requests
import config
from db.sql_helper import SqlHelper


class GetMyIPFail(Exception):

    def __str__(self):
        msg = 'Some error happened when try to get my ip :('
        return msg


def get_my_ip():
    '''获取自己的真实ip'''
    try:
        r = requests.get(
            url='http://ip.chinaz.com/getip.aspx', headers=config.HEADER,
            timeout=config.TIMEOUT)
        pattern = r'\d+\.\d+\.\d+\.\d+'
        match = re.search(pattern, r.text)
        if match:
            ip = match.group()
            return ip
        else:
            raise GetMyIPFail
    except:
        raise GetMyIPFail

def validate_proxy(proxy, my_ip, queue2=None):
    '''对代理进行检验(有效性，匿名性，连接时间)

    proxy为字典，必须包含的键：ip, port，其他键不作要求
    my_ip为字符串，表明本机真实ip

    queue2为队列2，用来存放成功经过检验后的代理
    每个队列元素为形式为:
    {'ip':ip, 'port':port, 'level':level}

    如果检测成功，返回经过检测修改后的proxy，字典形式
    （必定包含的键: ip, port, level）
    否则返回None'''
    ip = proxy['ip']
    port = proxy['port']
    proxies = {
        'http': 'http://{}:{}'.format(ip, port),
        'https': 'http://{}:{}'.format(ip, port)
    }
    try:
        r = requests.get(
            url='http://httpbin.org/get', headers=config.HEADER,
            timeout=config.TIMEOUT, proxies=proxies)
        if r.status_code == requests.codes.ok \
                and r.text.find('400 Bad Request') == -1:
            # 如果测试url的响应中检测不到本机真实ip，说明为匿名代理，否则算透明
            # （因为测试url考虑了XFF头，所以检测不到说明即高匿）
            if r.text.find(my_ip) == -1:
                proxy['level'] = 1
            else:
                proxy['level'] = 0
            # 如果给出了参数queue2，就将proxy加入其中
            if queue2:
                queue2.put(proxy)
        else:
            proxy = None
    except:
        proxy = None

    return proxy

def validate_proxy_in_db(proxy, my_ip, proxy_set):
    '''对代理进行检验并据此更新数据库

    proxy为字典，必须包含的键：ip, port，其他键不作要求
    my_ip为字符串，表明本机真实ip
    proxy_set为集合（用于去重），每个元素为'ip:port'形式的字符串

    无返回值'''
    validated_proxy = validate_proxy(proxy, my_ip)
    sqlhelper = SqlHelper()
    sqlhelper.init_db()
    # 如果检测成功，更新数据库对应条目
    # 否则删除数据库对应条目
    if validated_proxy:
        conditions = {
            'ip': proxy['ip'],
            'port': proxy['port']
        }
        # 稳定性+1
        old_stability = sqlhelper.select(
            conditions=conditions, show_stability=True)[0][2]
        new_stability = old_stability + 1
        # 经过检测成功后的validated_proxy字典必将还包括键: level
        value = {
            'level': validated_proxy['level'],
            'stability': new_stability,
        }
        sqlhelper.update(conditions, value)
        proxy_str = '{}:{}'.format(proxy['ip'], proxy['port'])
        proxy_set.add(proxy_str)
    else:
        conditions = {
            'ip': proxy['ip'],
            'port': proxy['port']
        }
        sqlhelper.delete(conditions)

def validate_between_queue(queue1, queue2):
    '''检验队列1中尚未经过检验的代理，将成功通过检验的添加到队列2中

    queue1为队列1，用来存放爬虫爬取到的尚未经过检验的代理（去重后）
    每个队列元素形式为：{'ip':ip, 'port':port}
    queue2为队列2，用来存放成功经过检验后的代理
    每个队列元素为形式为:
    {'ip':ip, 'port':port, 'level':level}

    无返回值'''
    task_list = []
    my_ip = get_my_ip()
    while True:
        try:
            proxy = queue1.get(timeout=10)
            task_list.append(proxy)
            if len(task_list) > 500:
                p = Process(
                    target=validate_task, args=(task_list, my_ip, queue2))
                p.start()
                task_list = []
        except:
            if len(task_list) > 0:
                p = Process(
                    target=validate_task, args=(task_list, my_ip, queue2))
                p.start()
                task_list = []

def validate_task(task_list, my_ip, queue2):
    '''validate_between_queue的进程调用函数

    task_list为列表，每个元素都是形式为{'ip':ip, 'port':port}的字典，为待检验的代理
    my_ip为字符串，表明本机的真实ip
    queue2为队列2，用来存放成功经过检验后的代理
    每个队列元素为形式为:
    {'ip':ip, 'port':port, 'level':level}

    无返回值'''
    spawns = []
    for task_proxy in task_list:
        spawns.append(gevent.spawn(validate_proxy, task_proxy, my_ip, queue2))
    gevent.joinall(spawns)