# -*- coding:utf-8 -*-

from app import db, app, engine
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
import sys,os,json
#尽量将id设置自增autoincrement，不设置添加过程中不带id无法加入
class PyCode(db.Model):
    __tablename__ =  'pycode'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), index=True)
    content = db.Column(db.String(2000))

    def __repr__(self):
        return '<name> %s' % self.name


class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), index=True)
    content = db.Column(db.JSON())
    setting = db.Column(db.JSON())

    def __repr__(self):
        return '<name> %s' % self.name

class GraphSetting(db.Model):
    __tablename__ = 'graphSetting'
    id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), index=True)
    note = db.Column(db.String(500), index=True)
    setting = db.Column(db.JSON())

    def __repr__(self):
        return '<name> %s' % self.name
   

class DBSession():
    def __init__(self,table_obj=None,data=None):
        self.table = table_obj
        self.data = data
        #不在网页上显示的数据库,如果新建了存在非直观数据的数据库也最好添加在里面
        self.hidden_db = ('information_schema','performance_schema','sys','mysql')
        self.json_cols = []

    def add(self):
        info = self.table_obj(**data)
        db.session.add(info)
        db.session.commit()

    def delete(self):
        pass

    def query(self):
        pass

    #以元组的方式返回
    def _uniform_query_res(self,res):
        new = []
        for i in res:
            new.append(i[0])
        return tuple(new)

    def execute_sql_query(self,sql,unif=True):
        cus = engine.connect()
        res = cus.execute(sql).fetchall()
        self
        cus.close()
        if unif:
            return self._uniform_query_res(res)
        else:
            return res

    def get_tables(self,database):
        #即便cus被关闭，他还是会记录上一次的选中的数据库
        cus = engine.connect()
        sql = 'use %s;' % database
        cus.execute(sql)
        cus.close()
        sql = 'show tables;'
        return self.execute_sql_query(sql)

    def get_databases(self):
        #需要剔除的mysql中自带的数据库
        
        sql = 'show databases;'
        res = list(self.execute_sql_query(sql))
        for i in self.hidden_db:
            try:
                res.remove(i)
            except ValueError:
                pass
        return tuple(res)

    def get_table_column_info(self,table_name):
        sql = 'desc %s;' % table_name
        cus = engine.connect()
        res = cus.execute(sql).fetchall()
        cus.close()
        return res
    
    def get_table_column(self,cols_info):
        self._check_json_column(cols_info)
        return self._uniform_query_res(cols_info)

    
    def get_sql_tree(self):
        cus = engine.connect()
        sql_tree = {}
        databases = self.get_databases()
        for i in databases:
            branch = {}
            tables = self.get_tables(i)
            for j in tables:
                cols_info = self.get_table_column_info(j)
                leaf = self.get_table_column(cols_info)
                branch[j] = leaf
            sql_tree[i] = branch
        return sql_tree

    def _check_json_column(self,cols_info):
        self.json_cols = []
        for i in cols_info:
            try:
                if i.Type=='json':
                    self.json_cols.append(i.Field)
            except AttributeError:
                print('获取表%s中的字段%stype信息出现错误' % (cols_info,i))

    #对存在json类型的数据进行解码，要求对象res为字典，因为RowProxy不能修改
    def _load_json(self,res):
        for i in self.json_cols:
            for j in res:
                j[i] = json.loads(j[i])

    def get_one_table(self,db,table):
        sql_1 = 'use %s;' % db
        # sql_2 = 'select * from %s where id >0;' % table
        sql_2 = 'select * from %s;' % table
        # [(1, 'xiaoao', '"{\\"a\\": 1, \\"b\\": 2}"', None),]

        cus = engine.connect()
        cus.execute(sql_1)
        content = cus.execute(sql_2).fetchall()
        cus.close()
        cols_info = self.get_table_column_info(table)
        table_cols = self.get_table_column(cols_info)
        # ('id', 'name', 'content', 'setting')
        res = [dict(x) for x in content]
        self._load_json(res)

        return {
            'main':res,
            'columns':table_cols
            }

class RunPy():
    def __init__(self,code=''):
        self.code = code
        self.main_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.target_file_path = os.path.join(self.main_path,'temp.py')
        self.front = 'import json,sys,traceback\n'
        self.result_contain = os.path.join(self.main_path,'temp_res.json')
        self.tail = """
with open(r'%s','w') as file:
    try:
        res = Query().solution()
        res = [dict(x) for x in res]
        file.write(json.dumps((res)))
        print('ok')
    except Exception as e:
        error = traceback.format_exc()
        file.write(json.dumps(error))
        print('error')
""" % self.result_contain
        

    def run(self):
        file = os.popen('python %s' %self.target_file_path)
        res = file.read().strip()#注意\n
        # print(res)
        
        file.close()
        if res=='ok':
            return True
        else:
            return False


    def write(self):

        with open(self.target_file_path,'w') as file:
            self.code = self.front + self.code + self.tail
            file.write(self.code)

    def read(self):
        with open(self.result_contain,'r') as file:
            res = json.loads(file.read())
        return res



            




    


     

