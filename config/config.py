# -*- coding: utf-8 -*-
# @Time    : 2021/4/20 下午7:28
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : config.py
# @Software: PyCharm

import os
import configparser
from datetime import timedelta

import redis

project_name = 'BaseCRM'


def get_config():
    """获取配置文件"""
    conf = configparser.ConfigParser()
    flask_env = os.environ.get('FLASK_ENV')
    base_path = os.getcwd().split(project_name)[0] + '{}/config/'.format(project_name)

    default_env = {
        'config_path': base_path + 'dev.ini',
        'msg': '本地配置文件:{}'.format(base_path + 'dev.ini'),
    }

    env_path_dict = {
        'default': default_env,
        'uat': {
            'config_path': base_path + 'uat.ini',
            'msg': 'uat配置文件:{}'.format(base_path + 'uat.ini'),
        },

        'production': {
            'config_path': base_path + 'pro.ini',
            'msg': 'prod配置文件:{}'.format(base_path + 'pro.ini')
        },
    }

    env_obj = env_path_dict.get(flask_env, default_env)
    msg = env_obj.get('msg')
    config_path = env_obj.get('config_path')
    print(msg)
    conf.read(config_path)
    return conf


class BaseConfig:
    """配置基类"""
    # SECRET_KEY = os.urandom(24)
    SECRET_KEY = 'ShaHeTop-Almighty-ares'  # session加密
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)  # 设置session过期时间
    DEBUG = True
    # SERVER_NAME = 'example.com'
    RUN_HOST = '0.0.0.0'
    RUN_PORT = 9999

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    """dev"""


class ProductionConfig(BaseConfig):
    """prod"""


class NewConfig(BaseConfig):
    """区分配置文件"""

    conf = get_config()  # 根据环境变量获取对应的配置文件

    # base
    SECRET_KEY = conf.get('base', 'SECRET_KEY')  # session加密
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)  # 设置session过期时间
    DEBUG = conf.getboolean('base', 'DEBUG')
    RUN_HOST = conf.get('base', 'RUN_HOST')
    RUN_PORT = conf.getint('base', 'RUN_PORT')

    # mysql
    DB_USERNAME = conf.get('mysql', 'USERNAME')
    DB_PASSWORD = conf.get('mysql', 'PASSWORD')
    DB_HOSTNAME = conf.get('mysql', 'HOSTNAME')
    DB_PORT = conf.getint('mysql', 'PORT')
    DB_DATABASE = conf.get('mysql', 'DATABASE')

    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
        conf.get('mysql', 'USERNAME'),
        conf.get('mysql', 'PASSWORD'),
        conf.get('mysql', 'HOSTNAME'),
        conf.getint('mysql', 'PORT'),
        conf.get('mysql', 'DATABASE')
    )
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    print(DB_URI)

    # redis
    redis_obj = {
        'host': conf.get('redis', 'REDIS_HOST'),
        'port': conf.get('redis', 'REDIS_PORT'),
        'password': conf.get('redis', 'REDIS_PWD'),
        'decode_responses': conf.getboolean('redis', 'DECODE_RESPONSES'),
        'db': conf.getint('redis', 'REDIS_DB')
    }
    POOL = redis.ConnectionPool(**redis_obj)
    R = redis.Redis(connection_pool=POOL)


config_obj = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'new': NewConfig
}

if __name__ == '__main__':
    cof = config_obj.get('new')()
