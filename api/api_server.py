# coding=utf-8

import sys
import json
import web
import config
from db.sql_helper import SqlHelper


sqlhelper = SqlHelper()
sqlhelper.init_db()

# URL映射关系
urls = (
    '/', 'select',
    '/delete', 'delete'
)

def start_api_server():
    '''启动api服务'''
    sys.argv.append('0.0.0.0:{}'.format(config.API_PORT))
    app = web.application(urls, globals())
    app.run()

class select():

    def GET(self):
        '''
        根据url参数的值进行数据库查询操作，最终以json字符串格式返回结果
        '''
        inputs = web.input()
        json_result = json.dumps(
            sqlhelper.select(inputs, inputs.get('count')))
        return json_result

class delete():

    def GET(self):
        '''
        根据url参数的值进行数据库删除操作，最终以json字符串格式返回结果
        '''
        inputs = web.input()
        json_result = json.dumps(sqlhelper.delete(inputs))
        return json_result