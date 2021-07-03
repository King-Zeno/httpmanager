# -*- coding: utf-8 -*-
__all__ = ['hrunmanage']
import pymysql
pymysql.version_info = (1, 4, 2, "final", 0)  #pymysql 添加 django 2.2 以上版本支持
pymysql.install_as_MySQLdb()