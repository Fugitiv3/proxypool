# coding=utf-8

import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, VARCHAR, Numeric, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
import config


Base = declarative_base()

class Proxy(Base):
    '''proxies表的映射类

    id: 表主键
    ip: 代理ip
    port: 代理端口
    level: 匿名程度（0:透明, 1:匿名）（高匿才算匿名，其他都算是透明）
    stability: 稳定性（整数，用成功经历过的检测次数来指示）
    updatetime: 上次检查更新的时刻'''

    __tablename__ = 'proxies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(VARCHAR(16), nullable=False)
    port = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False, default=0)
    stability = Column(Integer, nullable=False, default=1)
    updatetime = Column(DateTime(), default=datetime.datetime.utcnow())

class SqlHelper():
    '''SQL操作的基类'''
    params = {
        'ip': Proxy.ip,
        'port': Proxy.port,
        'level': Proxy.level,
        'stability': Proxy.stability,
        'updatetime': Proxy.updatetime
    }

    def __init__(self):
        '''初始化（创建session）'''
        self.engine = create_engine(
            config.DB_CONFIG['CONNECT_STRING'], echo=False,
            connect_args=config.DB_CONFIG['CONNECT_ARGS'])
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def init_db(self):
        '''初始化数据库

        调用create_all()会触发CREATE TABLE语句来创建表
        （已存在的表不会再创建）

        调用一次即可（多次调用也没有关系）'''
        Base.metadata.create_all(self.engine)

    def insert(self, value):
        '''执行插入操作

        value为字典，键为对应的列名，值为要插入的值
        必须包含的键: ip, port（level可以包含也可以省略）
        updatetime采用默认值即可'''
        proxy = Proxy(
            ip=value['ip'], port=value['port'], level=value.get('level'),
            stability=value.get('stability'))
        self.session.add(proxy)
        self.session.commit()

    def delete(self, conditions=None):
        '''执行删除操作

        删除满足对应条件的行

        conditions为字典形式，表明对应筛选条件
        如果为None，不删除任何行

        返回值为列表形式：{'delete_num':删除行数}'''
        condition_list = []
        if conditions:
            for key in conditions.keys():
                if self.params.get(key):
                    condition_list.append(
                        self.params.get(key)==conditions.get(key))
        if len(condition_list) > 0:
            query = self.session.query(Proxy)
            for condition in condition_list:
                query = query.filter(condition)
            delete_num = query.delete()
            self.session.commit()
        else:
            delete_num = 0
        return {'delete_num':delete_num}

    def select(self, conditions=None, count=None, show_stability=False):
        '''执行查询操作

        conditions为字典形式，键为对应的列名，值为对应筛选条件
        如果conditions为None，则不进行筛选（注意这里的行为与其他操作不同）

        count为整数，表明要返回的行数
        如果为None，返回满足条件的所有行

        show_stability为布尔值，指示返回结果中是否应该包含stability的值，默认为Fasle

        返回值为列表，每个元素为元组
        如果show_stability为False，列表中每个元组元素形式为(ip, port)
        否则，每个元素形式为(ip, port, stability)

        结果依次按stability降序排列'''
        condition_list = []
        if conditions:
            for key in conditions.keys():
                if self.params.get(key):
                    condition_list.append(
                        self.params.get(key)==conditions.get(key))
        if not show_stability:
            query = self.session.query(Proxy.ip, Proxy.port)
        else:
            query = self.session.query(Proxy.ip, Proxy.port, Proxy.stability)

        if len(condition_list) > 0 and count:
            for condition in condition_list:
                query = query.filter(condition)
            return query.order_by(
                Proxy.stability.desc()).limit(count).all()
        elif count:
            return query.order_by(
                Proxy.stability.desc()).limit(count).all()
        elif len(condition_list) > 0:
            for condition in condition_list:
                query = query.filter(condition)
            return query.order_by(
                Proxy.stability.desc()).all()
        else:
            return query.order_by(
                Proxy.stability.desc()).all()

    def update(self, conditions=None, value=None):
        '''执行更新操作

        conditions为字典形式，键为对应的列名，值为对应筛选条件
        如果conditions为None，不更新任何行

        value为字典，键为对应的列名，值为要更新的值
        （不用管updatetime，每次执行update操作时updatetime会自动更新）

        返回值为列表形式：{'update_num': 更新行数}'''
        condition_list = []
        if conditions and value:
            for key in conditions.keys():
                if self.params.get(key):
                    condition_list.append(
                        self.params.get(key)==conditions.get(key))
            for key in value.keys():
                if self.params.get(key) is None:
                    del value[key]

            if len(condition_list) > 0 and len(value) > 0:
                query = self.session.query(Proxy)
                for condition in condition_list:
                    query = query.filter(condition)
                # 自动设置更新时刻
                value['updatetime'] = datetime.datetime.utcnow()
                update_num = query.update(value)
                self.session.commit()
            else:
                update_num = 0
        else:
            update_num = 0
        return {'update_num':update_num}


def store_proxy(queue2):
    '''将队列2中的代理存入数据库中

    queue2为队列2，用来存放成功经过检验后的代理
    每个队列元素为形式为:
    {'ip':ip, 'port':port, 'level':level}'''
    sqlhelper = SqlHelper()
    sqlhelper.init_db()
    while True:
        proxy = queue2.get()
        sqlhelper.insert(proxy)