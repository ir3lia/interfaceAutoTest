# coding=utf-8
from pymongo import MongoClient
import json
import pymongo
from xml.sax.saxutils import escape
from bson.objectid import ObjectId
import time, datetime
import os
import sys
o_path = os.getcwd()  #返回当前工作目录
sys.path.append(o_path)  #添加自己指定的搜索路径
from utils import jsonRead
from utils import readYaml
from utils import readConfig

import sys

#获取config.yaml文件中数据库配置数据
commonConfig = readYaml.get_config("common/config.yaml", "dbInfo")
dbIP = commonConfig[1]["mongodbIp"]
dbPort = commonConfig[1]["mongodbPort"]
dbUser = commonConfig[1]["mongodbUser"]
dbPsw = commonConfig[1]["mongodbPsw"]

print(dbIP, dbPort, dbUser, dbPsw)

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        if not self.isEmpty():
            return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

# 插入ObjetcId数据
def saveOneData(database, coll, param):
    param = param.encode("utf-8")
    client = MongoClient(dbIP, dbPort)
    db=client.admin
    s=db.authenticate(dbUser, dbPsw)
    mydb = client[database]
    #mydb = client[database]
    collection = mydb[coll]
    s = Stack()
    param = json.loads(param)
    s.push(param)
    while not s.isEmpty():
        if type(s.peek()).__name__ == "list":
            e = s.pop()
            for i in e:
                s.push(i)
        if type(s.peek()).__name__ == 'dict':
            elem = s.pop()
            for k, v in elem.items():
                if type(v).__name__ == 'unicode':
                    v = v.encode("utf-8")
                if type(v).__name__ == 'dict' or type(v).__name__ == "list":
                    s.push(v)
                elif type(v).__name__ == 'str':
                    try:
                        elem[k] = datetime.datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
                    except Exception as e:
                        #print(str(e),"不是时间格式")
                        estr = str(e)
                    if k == '_id':
                        elem[k] = ObjectId(v)
                    elif v == "false":
                        elem[k] = False
                    elif v == "true":
                        elem[k] = True
        elif not s.isEmpty():
            s.pop()
    try:
        collection.insert_one(param)
    except Exception as e:
        print(str(e),"插入失败：唯一id冲突，请先执行删除！")
    return "SUCCEED"

# 插入非ObjetcId数据
def savetowData(database, coll, param):
    param = param.encode("utf-8")
    client = MongoClient(dbIP, dbPort)
    db=client.admin
    s=db.authenticate(dbUser, dbPsw)
    mydb = client[database]
    #mydb = client[database]
    collection = mydb[coll]
    s = Stack()
    param = json.loads(param)
    s.push(param)
    while not s.isEmpty():
        if type(s.peek()).__name__ == "list":
            e = s.pop()
            for i in e:
                s.push(i)
        if type(s.peek()).__name__ == 'dict':
            elem = s.pop()
            for k, v in elem.items():
                if type(v).__name__ == 'unicode':
                    v = v.encode("utf-8")
                if type(v).__name__ == 'dict' or type(v).__name__ == "list":
                    s.push(v)
                elif type(v).__name__ == 'str':
                    try:
                        elem[k] = datetime.datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
                    except ValueError:
                        "不是时间格式"
                    if v == "false":
                        elem[k] = False
                    elif v == "true":
                        elem[k] = True
        elif not s.isEmpty():
            s.pop()
    try:
        collection.insert_one(param)
    except Exception as e:
        print(str(e), "插入失败：唯一id冲突，请先执行删除！")

    return "SUCCEED"

#删除mongodb数据
def deleteMongodb(database,coll,param):
    param = param.encode("utf-8")
    client = pymongo.MongoClient(dbIP, dbPort)
    db = client['admin']
    db.authenticate(dbUser, dbPsw)
    mydb = client[database]
    collection = mydb[coll]
    #s = Stack()
    param = json.loads(param)

    result=collection.delete_many(param)
    print("删除成功数量：",result.deleted_count)

# 查询单条数据
def getOneData(database,coll,param,isObjectId):
    param = param.encode("utf-8")
    # 建立MongoDB数据库连接
    client = MongoClient(dbIP, dbPort)
    db=client.admin
    db.authenticate(dbUser, dbPsw)
    # 连接所需数据库,test为数据库名
    collection = client[database][coll]
    param = json.loads(param)
    if '_id' in param and isObjectId:
        param['_id'] = ObjectId(param['_id'])

    if collection.find_one(param) == None:
        return 'no data'
    else:
        # 查找集合中单条数据
        item = collection.find(param)
        #print("----------------haha------------------\n",type(item),"\n",list(item))
        #print("----------------haha------------------\n")
        result = list(item)
        #print("\n",len(result))
        #print(result)
        for i in range(len(result)):
            item = result[i]
            #print("----------------yeye------------------\n")
            item['_id'] = str(item['_id'])
            if 'createTime' in item:
                item['createTime'] = item['createTime'].strftime("%Y-%m-%d %H:%M:%S")
            if 'updateTime' in item:
                item['updateTime'] = item['updateTime'].strftime("%Y-%m-%d %H:%M:%S")
            if 'issuedDateTime' in item:
                item['issuedDateTime'] = item['issuedDateTime'].strftime("%Y-%m-%d %H:%M:%S")
            if 'createdTime' in item:
                item['createdTime'] = item['createdTime'].strftime("%Y-%m-%d %H:%M:%S")
            if 'updatedTime' in item:
                item['updatedTime'] = item['updatedTime'].strftime("%Y-%m-%d %H:%M:%S")

            #print(item)
        #item['_id'] = str(item['_id'])
        #result = json.dumps(item, ensure_ascii=False, default=str)
        #print("----------------xixi------------------\n",type(result),"\n",result)
        #print("----------------xixi------------------\n")
        return result

'''
@author: xiyang
@description: 根据json文件数据自动进行mongodb数据库操作
@params: 1、test_data_path表示json文件的路径；
         2、dataType表示操作的数据名称；
         3、oprType表示对数据库进行的操作类型，可选值有【delete,insert,all】,delete表示仅做清库操作，insert表示仅做插入操作，all表示先做delete再做insert
         4、caseNum可选参数，若测试用例需要指定数据库前后置数据，则需要传入对应的值
'''
def oprDatasToDB(test_data_path,dataType,oprType,caseNum=''):
    linkidDatas = jsonRead.loadDbData(test_data_path,dataType)
    database = linkidDatas['dbName']
    if caseNum=='':
        collectionData = linkidDatas['collectionData']
    else:
        collectionData = linkidDatas['collectionData'][caseNum]
    findList = []
    #print(linkidDatas,"\n",database,"\n",collectionData)
    print(oprType)
    for c in range(len(collectionData)):
        coll = collectionData[c]['collection']
        delDatas = collectionData[c]['deleteDatas']
        insertDatas = collectionData[c]['insertDatas']
        findDatas = collectionData[c]['findDatas']
        isObjectId = collectionData[c]['isObjectId']
        #print(delDatas,"\n",insertDatas,"\n",findDatas)
        #print(coll,"\n", len(delDatas))
        if oprType in ['delete','all']:
            for x in range(len(delDatas)):
                print("------------------------------delete",coll,x+1,"------------------------------")
                everyDelParam = delDatas[x]
                deleteMongodb(database,coll,json.dumps(everyDelParam))
                #print(everyDelParam)
        if oprType in ['insert','all']:
            print("是否objectId格式：",isObjectId)
            for y in range(len(insertDatas)):
                print("------------------------------insert",coll,y+1,"------------------------------")
                everyInsertParam = insertDatas[y]
                if isObjectId:
                    saveOneData(database,coll,json.dumps(everyInsertParam))
                else:
                    savetowData(database,coll,json.dumps(everyInsertParam))
                #print(everyInsertParam)
        if oprType in ['find']:
            for z in range(len(findDatas)):
                print("------------------------------find",coll,z+1,"------------------------------")
                everyfindParam = findDatas[z]
                finds = getOneData(database,coll,json.dumps(everyfindParam),isObjectId)
                print(finds,"\n",type(finds))
                if finds != "no data":
                    findList = findList + finds
                #print(everyfindParam)
    return findList


