# -*- coding:utf-8 -*-

from . import app, db
from flask import render_template,jsonify, request, abort, g
from app.models import PyCode, DBSession,RunPy,GraphSetting
from random import randint
import json


#测试前后端是否连接成功
@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1,100)
    }
    return jsonify(response)


#虽然任何没有被定义的路由都能用index.html展示，但是只有在为'/'时才有homepage字样
@app.route('/',defaults={"path": ''})#这个default什么意思
@app.route('/<path:path>')
#@app.route('/')
def catch_all(path):
    return render_template('index.html')
    # return 'Hello'

#接受前端来的Python代码，运行或者保存，或者均进行
@app.route('/api/postCode',methods=['GET','POST'])
def save_code_and_run():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        name = post_data.get('name')
        if name=='':
            response_object['message'] = 'name is empty!'
            return jsonify(response_object)
        
        data = {
            'name': name,
            'content': post_data.get('content')
        }
        if post_data.get('save'):
            response_object['type'] = 'save'
            code_id = post_data.get('id')
            if code_id:
                PyCode.query.filter_by(id=code_id).update(data)
                db.session.commit()
                response_object['message'] = 'pycode:<id>:%d is changed! ' % (code_id)
            else:
                p = PyCode(**data)
                db.session.add(p)
                db.session.commit()
                response_object['message'] = 'pycode:%s saved!' % post_data.get('name')
        if post_data.get('run'):
            response_object['type'] = 'run'
            rp = RunPy(data['content'])
            rp.write()
            is_ok = rp.run()
            result = rp.read()
            if is_ok:
                response_object['result'] = result
                response_object['isOk'] = True
                response_object['message'] = 'The query is executed successfully!'
            else:
                response_object['result'] = {}
                response_object['isOk'] = False
                response_object['message'] = result
            
    return jsonify(response_object)

#保存图表配置
@app.route('/api/postGraph',methods=['GET','POST'])
def save_and_read_graph():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        stem = post_data.get('setting')
        name = stem['title']['text']
        note = post_data.get('note')
        data = {
            'name':name,
            'setting':stem,
            'note':note,
        }
        setting = GraphSetting(**data)
        db.session.add(setting)
        db.session.commit()
        response_object['message'] = '%s:%s saved!' % (setting.__tablename__,post_data.get('name'))

    return jsonify(response_object)


#返回一个具体的表的内容
@app.route('/api/getdata',methods=['GET','POST'])
def get_sql_data():
    data = {}
    if request.method == 'GET':
        data = [
            {
                'name': '西啪啪',
                'role': 'cop'

            },
            {
                'name': 'Bod',
                'role': 'smith'
            }
        ]
    elif request.method == 'POST':
        data['status'] = 'success'

        post_data = request.get_json()
        db = post_data.get('db')
        table = post_data.get('table')
        data['jsonData'] = DBSession().get_one_table(db,table)

    else:
        data['status'] = 'success'
    result = jsonify(data)
    # with open(r't.json','w') as file:
    #     file.write(json.dumps(result))
    return result

#返回数据库整体树形目录
@app.route('/api/gettb',methods=['GET'])
def get_tbs():
    if request.method == 'GET':
        tables = DBSession().get_sql_tree()
        #将数据直接转为前端可以接受的数据
        def trans_tables_data(sql_data):
            res = []
            for i in sql_data:
                message = {
                    'db':i,
                    'tables':[x for x in sql_data[i].keys()]
                }
                res.append(message)
            return res

        data = trans_tables_data(tables)
    return jsonify(data)

@app.route('/api/delete_info',methods=['GET','POST'])
def delete_message():
    response_obj = {'status': 'success'}
    res = 0
    if request.method == 'POST':
        post_data = request.get_json()
        table_name = post_data.get('name')
        row_id = post_data.get('id')
        if table_name == 'pycode':

            res = PyCode.query.filter_by(id=row_id).delete()


        elif table_name == 'graphsetting':
            res = GraphSetting.query.filter_by(id=row_id).delete()
        else:
              response_obj['error'] = "没有找到对应的表格"
        db.session.commit()
        response_obj['success'] = bool(res)
    
    return jsonify(response_obj)








