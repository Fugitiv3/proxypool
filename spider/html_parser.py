# coding=utf-8

import re
import base64
import time
import logging
from lxml import etree
import requests
import config

class HTMLParser():
    '''用于HTML解析提取信息的类'''

    def __init__(self):
        '''初始化（配置记录网络请求日志）'''
        logging.basicConfig(
            format='[%(levelname)s] %(asctime)s:\r\n%(message)s\r\n',
            filename='requests.log', level=logging.INFO)

    def get_response(self, url, fuck_gfw=False):
        '''获取页面解码后的响应内容

        url为目标页面url
        fuck_gfw说明是否使用ss翻墙

        如果请求成功则返回页面解码后的响应内容
        否则返回None'''
        try:
            if fuck_gfw:
                r = requests.get(
                    url=url, headers=config.HEADER, timeout=config.TIMEOUT,
                    proxies=config.SS_PROXIES)
                return r.text
            else:
                r = requests.get(
                    url=url, headers=config.HEADER, timeout=config.TIMEOUT)
                return r.text
        except Exception as e:
            # 记录信息到日志中
            logging.info(
                'Something wrong when try to get the response of %s :\r\n%s',
                url, e)
            return None


    def parse(self, response, parser):
        '''解析页面响应内容

        response为解码后的页面响应内容
        parser为字典，参考config.PARSER_LIST中的元素

        返回值proxy_list为列表
        其中每个元素为字典，类似于：{'ip':ip, 'port': port}

        如果parser['type']不在选项中，返回None'''
        if parser['type'] == 'xpath':
            return self.xpath_parser(response, parser)
        elif parser['type'] == 'regular':
            return self.regular_parser(response, parser)
        elif parser['type'] == 'customized':
            return getattr(self, parser['function_name'])(response, parser)
        else:
            return None

    def xpath_parser(self, response, parser):
        '''针对xpath方式进行解析

        response编码后的页面响应内容
        parser为字典，参考config.PARSER_LIST中的元素

        返回值proxy_list为列表，其中每个元素为字典，类似于：
        {'ip':ip, 'port': port}'''
        proxy_list = []
        html = etree.HTML(response)
        proxy_elements = html.xpath(parser['pattern'])
        for proxy_element in proxy_elements:
            ip = proxy_element.xpath(parser['sub_pattern']['ip'])[0].text
            port = proxy_element.xpath(parser['sub_pattern']['port'])[0].text
            proxy = {'ip': ip, 'port': port,}
            proxy_list.append(proxy)
        return proxy_list

    def regular_parser(self, response, parser):
        '''针对正则表达式方式进行解析'''
        raise NotImplementedError

    def proxylist_parser(self, response, parser):
        '''专门解析https://proxy-list.org代理网站的函数

        response为解码后的页面响应内容
        parser为字典，参考config.PARSER_LIST中的元素

        返回值proxy_list为列表，其中每个元素为字典，类似于：
        {'ip':ip, 'port': port}'''
        proxy_list = []
        html = etree.HTML(response)
        encoded_proxy_elements = html.xpath(parser['pattern'])
        for encoded_proxy_element in encoded_proxy_elements:
            # print(encoded_proxy_element.text)
            match = re.search(
                r"'(.*?)'", encoded_proxy_element.text)
            if match:
                encoded_proxy_str = match.group(1)
                # print(encoded_proxy_str)
                proxy_str = base64.b64decode(encoded_proxy_str).decode('utf-8')
                # print(proxy_str)
                proxy = {
                    'ip': proxy_str.split(':')[0],
                    'port': proxy_str.split(':')[1],
                }
                proxy_list.append(proxy)
        return proxy_list