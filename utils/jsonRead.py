#coding=utf-8
import os
import sys
o_path = os.getcwd()  #返回当前工作目录
sys.path.append(o_path)  #添加自己指定的搜索路径
import json

def loadFont(test_data_path):
    f = open(test_data_path, encoding='utf-8')  #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    setting = json.load(f)
    return setting


def loadHttpData(test_data_path,dataType):
    case = []  # 存储测试用例名称
    description = []
    httpQuery = []  # 存储请求对象
    f = open(test_data_path, encoding='utf-8') #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    datas = json.load(f)
    d_200 = datas[dataType]
    for td in d_200:
        case.append(td['title'])
        description.append(td['otherInfo']['description'])
        httpQuery.append(td['httpData'])
    parameters = list(zip(case,description,httpQuery))
    return case,parameters

def loadDbData(db_data_path,dbName):
    f = open(db_data_path, encoding='utf-8') #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    datas = json.load(f)
    d = datas[dbName]
    return d

def getJsonKeyValue(jsonData):
    dataKey = []
    dataValue = []
    if isinstance(jsonData,dict):
        for key in jsonData:
            dataKey.append(key)
            dataValue.append(jsonData[key])
    return dataValue