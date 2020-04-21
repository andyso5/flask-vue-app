# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_cors import CORS

# import pymysql
# pymysql.install_as_MySQLdb()
app = Flask(__name__, template_folder='../../dist',static_folder='../../dist/static')
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] ="application/json;charset=utf-8"
#,template_folder='./templates'
cors = CORS(app, resources={"/api/*": {"origins": "*"}})#允许所有 /api/* 下的路由
# cors = CORS(app, resources={"*": {"origins": "*"}})
app.config.from_object('config')
db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


from . import models, views#有点意思