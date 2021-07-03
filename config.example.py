#coding=utf-8
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')

class Config:
    # base
    DEBUG = True    # docker 下运行需要设置为 False
    LEVEL = 'INFO'   # log level
    CACHE = False    # Django 缓存
    ALLOWED_HOSTS = ['*']

    # 数据库配置
    DATABASE = {
        'engine': 'mysql',
        'host': '127.0.0.1',
        'port': '3306',
        'user': 'root',
        'password': '123456',
        'dbname': 'hrunmanage'
    }

    # redis 缓存
    REDIS = {
        'host': '127.0.0.1',
        'port': '6379',
        'password': '123456',
        'db': '1'
    }

    # ldap
    AUTH_LDAP = True
    LDAP = {
        'host': "ldap://192.168.200.102",
        'bind_dn': "CN=ops,OU=Technology,DC=anlewo,DC=com",
        'password': "anlewo",
        'base_dn': "OU=Technology,DC=anlewo,DC=com"
    }

    # 邮件配置
    EMAIL = {
        "host": "smtp.anlewo.com",
        "port": 25,
        "user": "ops@anlewo.com",
        "password": "123456",
    }