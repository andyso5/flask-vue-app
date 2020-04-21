#-*- coding:utf-8 -*-

# 部署时需要运行

from app import db,engine
if __name__ == '__main__':
    # 创建数据库
    cur = engine.connect()
    cur.execute('create database rest;')


    db.create_all()
