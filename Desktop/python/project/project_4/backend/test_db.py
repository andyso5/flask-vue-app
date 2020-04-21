from app.models import PyCode,Data,DBSession,RunPy
from app import db
#from app import DBSession
import json
from pprint import pprint


def write_in_db(table_obj,data_dict):
    q = table_obj(**data_dict)#必须是一个字典
    db.session.add(q)
    db.session.commit()
    


def query_from_db(tale_obj,name):

    res = db.session.query(tale_obj).filter(tale_obj.name==name).all()
    return res



if __name__ == '__main__':
    
    # data = {
    #     'name':'xiaoao',
    #     'content':'from pprint import pprint\npprint("fine,thanks'
    # }
    # write_in_db(PyCode,data)


    # json_data = json.dumps({'a':1,'b':2})
    # data = {
    #     'name':'xiaoao',
    #     'content':json_data
    # }
    # write_in_db(Data,data)


    # res = query_from_db(Data,'xiaoao')
    # print(json.loads(res[0].content))

    # pprint(DBSession().get_sql_tree())#获得整个数据库的结构
    # {'rest': {'data': ('id', 'name', 'content', 'setting'),
    #       'migrate_version': ('repository_id', 'repository_path', 'version'),
    #       'pycode': ('id', 'name', 'content'),
    #       'users': ('id', 'username', 'password')}}
    # pprint(DBSession().get_one_table('rest','pycode'))

#     [{'content': 'from pprint import pprint\npprint("fine,thanks")',
#   'name': 'xiaoao'},
#  {'content': 'class Query():\n    def solution():', 'name': 'test'},
#  {'content': 'class Query():\n    def solution():\nlllll', 'name': 'newbee'}]


    # code = """from app import engine\nclass Query():\n\tdef solution(self):\n\t\treturn {'a':1,'b':2}"""
    # RP = RunPy(code)
    # RP.write()
    # res = RP.run()
    # print(RP.read().keys())
    # print(res)

    # import os
    # file

    print(PyCode.query.filter_by(PyCode.name='cccc').delete())