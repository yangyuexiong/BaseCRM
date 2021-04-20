# -*- coding: utf-8 -*-
# @Time    : 2021/4/20 下午8:11
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : tools.py
# @Software: PyCharm

import json
import socket

import pymysql

from config.config import config_obj

CONFIG_OBJ = config_obj.get('new')
R = CONFIG_OBJ.R
DB_USERNAME = CONFIG_OBJ.DB_USERNAME
DB_PASSWORD = CONFIG_OBJ.DB_PASSWORD
DB_HOSTNAME = CONFIG_OBJ.DB_HOSTNAME
DB_PORT = CONFIG_OBJ.DB_PORT
DB_DATABASE = CONFIG_OBJ.DB_DATABASE
DB = {
    'user': DB_USERNAME,
    'password': DB_PASSWORD,
    'host': DB_HOSTNAME,
    'port': DB_PORT,
    'db': DB_DATABASE
}


def check_keys(dic, *keys):
    for k in keys:
        if k not in dic.keys():
            return False
    return True


def jd(kv):
    """序列化中文显示简化"""
    if isinstance(kv, dict):
        return json.dumps(kv, ensure_ascii=False)
    else:
        return kv


def json_format(json_obj):
    """
    json打印格式化
    :param json_obj:json对象/dict
    :return:
    """
    try:
        print(json.dumps(json_obj, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
    except BaseException as e:
        print(json_obj)


def get_host_ip():
    """
    获取本机IP
    :return:
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    return ip


class MyPyMysql:
    def __init__(self, host=None, port=None, user=None, password=None, db=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    def db_obj(self):
        """
        返回db对象
        :return:
        """
        try:
            database_obj = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db)
            return database_obj
        except BaseException as e:
            return '连接数据库参数异常{}'.format(str(e))

    def create_data(self, sql=None):
        """
        新增
        :return:
        """
        try:
            db = self.db_obj()
            with db.cursor() as cur:
                print(sql)
                cur.execute(sql)
                db.commit()
                return 'create success'
        except BaseException as e:
            cur.rollback()
            return 'create:出现错误:{}'.format(str(e))

    def read_data(self, sql=None):
        """
        查询(废弃,保留实现思想)(使用: MyPyMysql.select 代替之)
        :param sql:
        :return:
        """
        try:
            db = self.db_obj()
            with db.cursor() as cur:
                cur.execute(sql)  # 执行sql语句
                # sql = "select * from gambler where id='YfpgoLZtEGPfMXUvFPffCi'"

                '''
                获取表结构,并且取出字段,生成列表
                '''
                '''获取字段列表'''
                # print(cur.description)
                key_list = [i[0] for i in cur.description]
                # print(key_list)

                '''
                把查询结果集组装成列表
                '''
                results = cur.fetchall()
                # print(results)
                data_list = [i for i in results]
                # print(data_list)

                data_dict = []
                for field in cur.description:
                    data_dict.append(field[0])
                # print(data_dict)
                # print(len(data_dict))

                '''
                将字段与每一条查询数据合并成键值对,并且组装成新的列表
                new_list = []
                for i in data_list:
                    print(list(i))
                    new_list.append(dict(zip(key_list, list(i))))
                '''
                new_list = [dict(zip(key_list, list(i))) for i in data_list]
                # print(new_list)
                return new_list
        except BaseException as e:
            return 'read:出现错误:{}'.format(str(e))

    def update_data(self, sql=None):
        """
        更新
        :param sql:
        :return:
        """
        try:
            db = self.db_obj()
            with db.cursor() as cur:
                cur.execute(sql)
                db.commit()
                return 'update success'
        except BaseException as e:
            cur.rollback()
            return 'update:出现错误:{}'.format(str(e))

    def del_data(self, sql=None):
        """
        删除
        :param sql:
        :return:
        """
        try:
            db = self.db_obj()
            with db.cursor() as cur:
                cur.execute(sql)
                db.commit()
                return 'del success'
        except BaseException as e:
            cur.rollback()
            return 'del:出现错误:{}'.format(str(e))

    def select(self, sql=None, only=None, size=None):
        """
        查询
        :param sql:
        :param only:
        :param size:
        :return:
        """
        try:
            db = self.db_obj()
            with db.cursor(pymysql.cursors.DictCursor) as cur:
                cur.execute(sql)  # 执行sql语句
                # sql = "select * from gambler where id='YfpgoLZtEGPfMXUvFPffCi'"
                if only and not size:  # 唯一结果返回 json/dict
                    rs = cur.fetchone()
                    return rs
                if size and not only:  # 按照需要的长度返回
                    rs = cur.fetchmany(size)
                    return rs
                else:  # 返回结果集返回 list
                    rs = cur.fetchall()
                    return rs
        except BaseException as e:
            return 'select:出现错误:{}'.format(str(e))


tp_db = MyPyMysql(**DB)
