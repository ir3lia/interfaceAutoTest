import json
import ast
from jsonpath_rw import jsonpath, parse
import os
import sys
o_path = os.getcwd()  #返回当前工作目录
sys.path.append(o_path)  #添加自己指定的搜索路径
from utils import jsonRead

#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@author: xiyang
'''

class HandleJson():
  def __init__(self, data):
    if data == None:
      print('请输入json格式数据')
      exit()
 
    if isinstance(data, str):
      try:
        self.data = ast.literal_eval(data)
      except:
        print('请输入正确的json格式数据')
        exit()
    elif isinstance(data, dict):
      self.data = data
 
  def __paths(self, data, path=''):
    '''
    用于遍历json树
    :param data: 原始数据，或者key对应的value值
    :param path: key值字符串，默认值为''
    :return:
    '''
    if isinstance(data, dict):
      for k, v in data.items():
        tmp = path + "['%s']" % k
        yield (tmp, v)
        yield from self.__paths(v, tmp)
 
    if isinstance(data, list):
      for k, v in enumerate(data):
        tmp = path + '[%d]' % k
        yield (tmp, v)
        yield from self.__paths(v, tmp)
 
  def find_key_path(self, key):
    '''
    查找key路径
    :param key: 需要查找路径的key值
    :return: 包含key值路径的list
    '''
    result = []
    for path,value in self.__paths(self.data):
      if path.endswith("['%s']" % key):
        result.append(path)
    with open('path.txt', 'w+', encoding='utf-8') as f:
      list(map(lambda line: f.write(line + '\r'), result))
    return result
 
  def find_value_path(self, key):
    '''
    查找某个值的路径
    :param key: 需要查找的值，限制为字符串，数字，浮点数，布尔值
    :return:
    '''
    result = []
    for path, value in self.__paths(self.data):
      if isinstance(value, (str, int, bool, float)):
        if value == key:
          result.append(path)
    with open('path.txt', 'w+', encoding='utf-8') as f:
      list(map(lambda line: f.write(line + '\r'), result))
    return result

class JsonKey:
  def __init__(self):
      self.key_list = []
  def get_dict_allkeys(self,dict_a):
    """
    遍历嵌套字典，获取json返回结果的所有key值
    :param dict_a:
    :return: key_list
    """
    if isinstance(dict_a, dict):  # 使用isinstance检测数据类型
        # 如果为字典类型，则提取key存放到key_list中
        for x in range(len(dict_a)):
            temp_key = list(dict_a.keys())[x]
            temp_value = dict_a[temp_key]
            if not isinstance(temp_value, dict) and not isinstance(temp_value, list):
                self.key_list.append(temp_key)
            elif isinstance(temp_value, list):
                 for k in temp_value:
                     if not isinstance(k, dict):
                         self.key_list.append(temp_key)
                         break
            self.get_dict_allkeys(temp_value)  # 自我调用实现无限遍历
    elif isinstance(dict_a, list):
        # 如果为列表类型，则遍历列表里的元素，将字典类型的按照上面的方法提取key
        for k in dict_a:
            if isinstance(k, dict):
                for x in range(len(k)):
                    temp_key = list(k.keys())[x]
                    temp_value = k[temp_key]
                    if not isinstance(temp_value, dict) and not isinstance(temp_value, list):
                        self.key_list.append(temp_key)
                    elif isinstance(temp_value, list):
                        for k in temp_value:
                            if not isinstance(k, dict):
                                self.key_list.append(temp_key)
                                break
                    self.get_dict_allkeys(temp_value) # 自我调用实现无限遍历
    return self.key_list

def deDuplication(list_a):
    keys = []
    for id in list_a:
        if id not in keys:
            keys.append(id)
    return keys

def getKeyPaths(json_data):
    hj = HandleJson(json_data)
    jk = JsonKey()
    get_keys = jk.get_dict_allkeys(json_data)
    #print("-------------------叶节点key-",get_keys)
    list_keys = deDuplication(get_keys)
    keyPaths = []
    for x in list_keys:
        res = hj.find_key_path(x)
        keyPaths.extend(res)
    return keyPaths

def getKeyValues(json_data,json_path):
    #res1 = jsonpath.jsonpath(json_data,"$"+json_path)
    res1 = [match.value for match in parse(json_path).find(json_data)]
    return res1

def getStringParams(json_data):
  allValues = jsonRead.getJsonKeyValue(json_data)
  stringParams = ''
  for i in range(len(allValues)):
    stringParams = stringParams + '/' + allValues[i]
  return stringParams
 
if __name__ == '__main__': 
  print("--------------haha---------")