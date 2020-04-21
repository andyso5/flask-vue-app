import json,sys,traceback
from app import engine
cur = engine.connect()
class Query():
	def solution(self):
		sqls = ['select * from sale where id > 1;']
		for i in sqls:
			res = cur.execute(i)
		return res.fetchall()

with open(r'c:\Users\Administrator\Desktop\python\project\project_4\backend\temp_res.json','w') as file:
    try:
        res = Query().solution()
        res = [dict(x) for x in res]
        file.write(json.dumps((res)))
        print('ok')
    except Exception as e:
        error = traceback.format_exc()
        file.write(json.dumps(error))
        print('error')
