import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017")
print(client.list_database_names())
db = client['test']
collection = db['test']
stu1={'id':'001','name':'zhangsan','age':10}
result = collection.insert_one(stu1)
stu2={'id':'002','name':'lisi','age':15}
stu3={'id':'003','name':'wangwu','age':20}
result = collection.insert_many([stu2,stu3])
# #可以直接使用remove方法删除指定的数据
# result = collection.remove({'name': 'zhangsan'})
# #使用delete_one()删除一条数据
# result = collection.delete_one({"name":"zhangsan"})
# #delete_many()删除多条数据
# result = collection.delete_many({"age":{'$lt':20}})
# condition = {'name': 'zhangsan'}
# res = collection.find_one(condition)
# res['age'] = 22
# result = collection.update_one(condition, {'$set': res})
# print(result) #返回结果是UpdateResult类型
# print(result.matched_count,result.modified_count) #获得匹配的数据条数1、影响的数据条数1

# #update_many,所有年龄为15的name修改为xixi
# condition = {'age': 15}
# res = collection.find_one(condition)
# res['age'] = 30
# result = collection.update_many(condition, {'$set':{'name':'xixi'}})
# print(result) #返回结果是UpdateResult类型
# print(result.matched_count,result.modified_count) #获得匹配的数据条数3、影响的数据条数3

rets = collection.find({"age":20})
for ret in rets:
    print(ret)

# 查询结果按年龄升序排序
results = collection.find().sort('age', pymongo.ASCENDING)
print([result['age'] for result in results])

ret =collection.find_one({'name': 'zhangsan'})
print(ret)
