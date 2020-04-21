# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))
user = 'root'
password = '074057'
#从数据库获取的数据编码方式，到后端发送的数据编码方式，再到前端解码方式，应保持一致
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@localhost:3306/rest?charset=UTF8MB4" %(user,password)

SQLALCHEMY_TRACK_MODIFICATIONS = True

