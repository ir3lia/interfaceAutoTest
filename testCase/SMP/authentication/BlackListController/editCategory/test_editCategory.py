#coding=utf-8
import os
import sys
o_path = os.getcwd()  #返回当前工作目录
sys.path.append(o_path)  #添加自己指定的搜索路径
import unittest
import pytest
import allure
import json
import requests
import yaml
from jsonpath_rw import jsonpath, parse
from utils import readYaml
from utils import jsonRead
from utils import jsonAnalysis
from utils import mongoDataOpr
from utils import httpApi
from utils import checkConnect

testerName = 'sunxiaojian'
controllerName = "BlackListController"
interfaceChName = "修改黑名单提示信息"
interfaceEnName = "editInfoMessage"

commonConfig = readYaml.get_config("common/config.yaml", "common") #返回config.yaml文件中的common数组的所有数据
authenticationApiPaths = readYaml.get_apiPath("common/apiPaths/authenticationPath.yaml")  # 返回linkidPath.yaml文件中的所有linkid接口路径
urlIP = commonConfig[0]["linkidIP"]
urlPath = authenticationApiPaths[0]['editInfoMessage']

dirPath, fileName = os.path.split(os.path.abspath(__file__))
cases_main,parameters_main = jsonRead.loadHttpData(dirPath + "/testData.json", 'mainCaseData') #读取主流程测试数据
cases_all,parameters_all = jsonRead.loadHttpData(dirPath + "/testData.json", 'allCaseData') #读取所有测试数据
dbJsonPath = dirPath + "/dbData.json"  #获取数据库设计数据
dbName = "authentication" #数据库设计中对应的组件

@allure.epic(controllerName)
@allure.feature(interfaceChName)
class Test_class():

    @allure.story(interfaceChName + "-主流程")
    @allure.title("{case}")
    @pytest.mark.dependency(name=interfaceEnName + "_main")
    @pytest.mark.parametrize("case,description,httpParameters", list(parameters_main))
    def test_main(self, case, description, httpParameters):
        allure.attach('{0}'.format(testerName), "测试人员")
        allure.attach(json.dumps(httpParameters["query"], ensure_ascii=False), "接口入参")  # 测试用例的入参
        if 'caseNum' in httpParameters:
            print("\n ==清理数据库 & 插入数据==")
            mongoDataOpr.oprDatasToDB(dbJsonPath, dbName, "all", httpParameters["caseNum"])
        if httpParameters["paramType"] == "string":
            stringParams = jsonAnalysis.getStringParams(httpParameters["query"])
            urlPath2 = urlPath + stringParams + "/editCategory?" + "blackListCategory=USER_MAC_SPECIFIC&lastModifiedUser=admin&nodeMac=AA-BB-BB-BB-BB-BB&userObjectId=5f17e3486227f3000629a7a5"
            postJ = httpApi.httpRequests(urlIP, urlPath2, httpParameters["httpType"])
        elif httpParameters["paramType"] == "json":
            urlPath3 = urlPath + "?lastModifiedUser=admin"
            postJ = httpApi.httpRequests(urlIP, urlPath3, httpParameters["httpType"], parame=httpParameters["query"])
        else:
            assert 0, '参数类型「' + httpParameters["paramType"] + '」无法处理！'
        allure.attach("{0}".format(postJ), "接口出参")  # 测试用例的出参
        # 获取json中的所有叶节点key的路径
        keyPaths = jsonAnalysis.getKeyPaths(httpParameters["response"])
        for path in keyPaths:
            # 通过path获取对应的value
            res1 = jsonAnalysis.getKeyValues(httpParameters["response"], path)
            res2 = jsonAnalysis.getKeyValues(postJ, path)
            assert len(res2) > 0, path + "不存在"
            assert res1 == res2, path + " 值错误！"
        if httpParameters["isCheckDB"]:
            haha = mongoDataOpr.oprDatasToDB(dbJsonPath, dbName, "find")
            if httpParameters["checkDBType"] == "exist":
                assert len(haha) == 1
            if httpParameters["checkDBType"] == "non-exist":
                assert haha == []

    @allure.story(interfaceChName + "-测试用例")
    @allure.title("{case}")
    @pytest.mark.dependency(name=interfaceEnName + "_all", depends=[interfaceEnName + "_main"])
    @pytest.mark.parametrize("case,description,httpParameters", list(parameters_all))
    def test_all(self, case, description, httpParameters):
        allure.attach('{0}'.format(testerName), "测试人员")
        allure.attach(json.dumps(httpParameters["query"], ensure_ascii=False), "接口入参")  # 测试用例的入参
        if 'caseNum' in httpParameters:
            print("\n ==清理数据库 & 插入数据==")
            mongoDataOpr.oprDatasToDB(dbJsonPath, dbName, "all", httpParameters["caseNum"])
        if httpParameters["paramType"] == "string":
            stringParams = jsonAnalysis.getStringParams(httpParameters["query"])
            urlPath2 = urlPath + stringParams + "/editCategory?" + "blackListCategory=MAC_SPECIFIC&lastModifiedUser=afeng&nodeMac=AA-BB-BB-BB-BB-BB&userObjectId=5f17e3486227f3000629a7a5"
            postJ = httpApi.httpRequests(urlIP, urlPath2, httpParameters["httpType"])
        elif httpParameters["paramType"] == "json":
            urlPath3 = urlPath + "?lastModifiedUser=afeng"
            postJ = httpApi.httpRequests(urlIP, urlPath3, httpParameters["httpType"], parame=httpParameters["query"])
        else:
            assert 0, '参数类型「' + httpParameters["paramType"] + '」无法处理！'
        allure.attach("{0}".format(postJ), "接口出参")  # 测试用例的出参
        keyPaths = jsonAnalysis.getKeyPaths(httpParameters['response'])
        for path in keyPaths:
            res1 = jsonAnalysis.getKeyValues(httpParameters["response"], path)
            res2 = jsonAnalysis.getKeyValues(postJ, path)
            assert len(res2) > 0, path + "不存在"
            assert res1 == res2, path + " 值错误！"
        if httpParameters["isCheckDB"]:
            haha = mongoDataOpr.oprDatasToDB(dbJsonPath, dbName, "find")
            if httpParameters["checkDBType"] == "exist":
                assert len(haha) == 1
            if httpParameters["checkDBType"] == "non-exist":
                assert haha == []

    @allure.story(interfaceChName + "-测试用例")
    @allure.title("{case}")
    @pytest.mark.dependency(name=interfaceEnName + "_all", depends=[interfaceEnName + "_main"])
    @pytest.mark.parametrize("case,description,httpParameters", list(parameters_all))
    def test_all(self, case, description, httpParameters):
        allure.attach('{0}'.format(testerName), "测试人员")
        allure.attach(json.dumps(httpParameters["query"], ensure_ascii=False), "接口入参")  # 测试用例的入参
        if 'caseNum' in httpParameters:
            print("\n ==清理数据库 & 插入数据==")
            mongoDataOpr.oprDatasToDB(dbJsonPath, dbName, "all", httpParameters["caseNum"])
        if httpParameters["paramType"] == "string":
            stringParams = jsonAnalysis.getStringParams(httpParameters["query"])
            urlPath2 = urlPath + stringParams + "/editCategory?" + "blackListCategory=USER_MAC_SPECIFIC&lastModifiedUser=afeng&nodeMac=AA-BB-CC-BB-BB-BB&userObjectId=5f17e3486227f3000629a7a5"
            postJ = httpApi.httpRequests(urlIP, urlPath2, httpParameters["httpType"])
        elif httpParameters["paramType"] == "json":
            urlPath3 = urlPath + "?lastModifiedUser="
            postJ = httpApi.httpRequests(urlIP, urlPath3, httpParameters["httpType"], parame=httpParameters["query"])
        else:
            assert 0, '参数类型「' + httpParameters["paramType"] + '」无法处理！'
        allure.attach("{0}".format(postJ), "接口出参")  # 测试用例的出参
        keyPaths = jsonAnalysis.getKeyPaths(httpParameters['response'])
        for path in keyPaths:
            res1 = jsonAnalysis.getKeyValues(httpParameters["response"], path)
            res2 = jsonAnalysis.getKeyValues(postJ, path)
            assert len(res2) > 0, path + "不存在"
            assert res1 == res2, path + " 值错误！"
        if httpParameters["isCheckDB"]:
            haha = mongoDataOpr.oprDatasToDB(dbJsonPath, dbName, "find")
            if httpParameters["checkDBType"] == "exist":
                assert len(haha) == 1
            if httpParameters["checkDBType"] == "non-exist":
                assert haha == []

    @allure.story(interfaceChName + "-测试用例")
    @allure.title("{case}")
    @pytest.mark.dependency(name=interfaceEnName + "_all", depends=[interfaceEnName + "_main"])
    @pytest.mark.parametrize("case,description,httpParameters", list(parameters_all))
    def test_all(self, case, description, httpParameters):
        allure.attach('{0}'.format(testerName), "测试人员")
        allure.attach(json.dumps(httpParameters["query"], ensure_ascii=False), "接口入参")  # 测试用例的入参
        if 'caseNum' in httpParameters:
            print("\n ==清理数据库 & 插入数据==")
            mongoDataOpr.oprDatasToDB(dbJsonPath, dbName, "all", httpParameters["caseNum"])
        if httpParameters["paramType"] == "string":
            stringParams = jsonAnalysis.getStringParams(httpParameters["query"])
            urlPath2 = urlPath + stringParams + "/editCategory?" + "blackListCategory=USER_SPECIFIC&lastModifiedUser=afengda&userObjectId=5f17e3486227f3000629a711"
            postJ = httpApi.httpRequests(urlIP, urlPath2, httpParameters["httpType"])
        elif httpParameters["paramType"] == "json":
            urlPath3 = urlPath + "?lastModifiedUser="
            postJ = httpApi.httpRequests(urlIP, urlPath3, httpParameters["httpType"], parame=httpParameters["query"])
        else:
            assert 0, '参数类型「' + httpParameters["paramType"] + '」无法处理！'
        allure.attach("{0}".format(postJ), "接口出参")  # 测试用例的出参
        keyPaths = jsonAnalysis.getKeyPaths(httpParameters['response'])
        for path in keyPaths:
            res1 = jsonAnalysis.getKeyValues(httpParameters["response"], path)
            res2 = jsonAnalysis.getKeyValues(postJ, path)
            assert len(res2) > 0, path + "不存在"
            assert res1 == res2, path + " 值错误！"
        if httpParameters["isCheckDB"]:
            haha = mongoDataOpr.oprDatasToDB(dbJsonPath, dbName, "find")
            if httpParameters["checkDBType"] == "exist":
                assert len(haha) == 1
            if httpParameters["checkDBType"] == "non-exist":
                assert haha == []

    @allure.story(interfaceChName + "-测试用例")
    @allure.title("{case}")
    @pytest.mark.dependency(name=interfaceEnName + "_all", depends=[interfaceEnName + "_main"])
    @pytest.mark.parametrize("case,description,httpParameters", list(parameters_all))
    def test_all(self, case, description, httpParameters):
        allure.attach('{0}'.format(testerName), "测试人员")
        allure.attach(json.dumps(httpParameters["query"], ensure_ascii=False), "接口入参")  # 测试用例的入参
        if 'caseNum' in httpParameters:
            print("\n ==清理数据库 & 插入数据==")
            mongoDataOpr.oprDatasToDB(dbJsonPath, dbName, "all", httpParameters["caseNum"])
        if httpParameters["paramType"] == "string":
            stringParams = jsonAnalysis.getStringParams(httpParameters["query"])
            urlPath2 = urlPath + stringParams + "/editCategory?" + "blackListCategory=MAC_SPECIFIC&lastModifiedUser=admin&nodeMac=AA-BB-CC-BB-BB-BB"
            postJ = httpApi.httpRequests(urlIP, urlPath2, httpParameters["httpType"])
        elif httpParameters["paramType"] == "json":
            urlPath3 = urlPath + "?lastModifiedUser="
            postJ = httpApi.httpRequests(urlIP, urlPath3, httpParameters["httpType"], parame=httpParameters["query"])
        else:
            assert 0, '参数类型「' + httpParameters["paramType"] + '」无法处理！'
        allure.attach("{0}".format(postJ), "接口出参")  # 测试用例的出参
        keyPaths = jsonAnalysis.getKeyPaths(httpParameters['response'])
        for path in keyPaths:
            res1 = jsonAnalysis.getKeyValues(httpParameters["response"], path)
            res2 = jsonAnalysis.getKeyValues(postJ, path)
            assert len(res2) > 0, path + "不存在"
            assert res1 == res2, path + " 值错误！"
        if httpParameters["isCheckDB"]:
            haha = mongoDataOpr.oprDatasToDB(dbJsonPath, dbName, "find")
            if httpParameters["checkDBType"] == "exist":
                assert len(haha) == 1
            if httpParameters["checkDBType"] == "non-exist":
                assert haha == []

    @allure.story(interfaceChName + "-测试用例")
    @allure.title("{case}")
    @pytest.mark.dependency(name=interfaceEnName + "_all", depends=[interfaceEnName + "_main"])
    @pytest.mark.parametrize("case,description,httpParameters", list(parameters_all))
    def test_all(self, case, description, httpParameters):
        allure.attach('{0}'.format(testerName), "测试人员")
        allure.attach(json.dumps(httpParameters["query"], ensure_ascii=False), "接口入参")  # 测试用例的入参
        if 'caseNum' in httpParameters:
            print("\n ==清理数据库 & 插入数据==")
            mongoDataOpr.oprDatasToDB(dbJsonPath, dbName, "all", httpParameters["caseNum"])
        if httpParameters["paramType"] == "string":
            stringParams = jsonAnalysis.getStringParams(httpParameters["query"])
            urlPath2 = urlPath + stringParams + "/editCategory?" + "blackListCategory=MAC_SPECIFIC&lastModifiedUser=admin&nodeMac=AA-BB-CC-BB-BB-BB"
            postJ = httpApi.httpRequests(urlIP, urlPath2, httpParameters["httpType"])
        elif httpParameters["paramType"] == "json":
            urlPath3 = urlPath + "?lastModifiedUser="
            postJ = httpApi.httpRequests(urlIP, urlPath3, httpParameters["httpType"], parame=httpParameters["query"])
        else:
            assert 0, '参数类型「' + httpParameters["paramType"] + '」无法处理！'
        allure.attach("{0}".format(postJ), "接口出参")  # 测试用例的出参
        keyPaths = jsonAnalysis.getKeyPaths(httpParameters['response'])
        for path in keyPaths:
            res1 = jsonAnalysis.getKeyValues(httpParameters["response"], path)
            res2 = jsonAnalysis.getKeyValues(postJ, path)
            assert len(res2) > 0, path + "不存在"
            assert res1 == res2, path + " 值错误！"
        if httpParameters["isCheckDB"]:
            haha = mongoDataOpr.oprDatasToDB(dbJsonPath, dbName, "find")
            if httpParameters["checkDBType"] == "exist":
                assert len(haha) == 1
            if httpParameters["checkDBType"] == "non-exist":
                assert haha == []

    @allure.story(interfaceChName + "-测试用例")
    @allure.title("{case}")
    @pytest.mark.dependency(name=interfaceEnName + "_all", depends=[interfaceEnName + "_main"])
    @pytest.mark.parametrize("case,description,httpParameters", list(parameters_all))
    def test_all(self, case, description, httpParameters):
        allure.attach('{0}'.format(testerName), "测试人员")
        allure.attach(json.dumps(httpParameters["query"], ensure_ascii=False), "接口入参")  # 测试用例的入参
        if 'caseNum' in httpParameters:
            print("\n ==清理数据库 & 插入数据==")
            mongoDataOpr.oprDatasToDB(dbJsonPath, dbName, "all", httpParameters["caseNum"])
        if httpParameters["paramType"] == "string":
            stringParams = jsonAnalysis.getStringParams(httpParameters["query"])
            urlPath2 = urlPath + stringParams + "/editCategory?" + "blackListCategory=USER_MAC_SPECIFIC&lastModifiedUser=admin&nodeMac=AA-BB-CC-BB-BB-BB&userObjectId=5f17e3486227f3000629a711"
            postJ = httpApi.httpRequests(urlIP, urlPath2, httpParameters["httpType"])
        elif httpParameters["paramType"] == "json":
            urlPath3 = urlPath + "?lastModifiedUser="
            postJ = httpApi.httpRequests(urlIP, urlPath3, httpParameters["httpType"], parame=httpParameters["query"])
        else:
            assert 0, '参数类型「' + httpParameters["paramType"] + '」无法处理！'
        allure.attach("{0}".format(postJ), "接口出参")  # 测试用例的出参
        keyPaths = jsonAnalysis.getKeyPaths(httpParameters['response'])
        for path in keyPaths:
            res1 = jsonAnalysis.getKeyValues(httpParameters["response"], path)
            res2 = jsonAnalysis.getKeyValues(postJ, path)
            assert len(res2) > 0, path + "不存在"
            assert res1 == res2, path + " 值错误！"
        if httpParameters["isCheckDB"]:
            haha = mongoDataOpr.oprDatasToDB(dbJsonPath, dbName, "find")
            if httpParameters["checkDBType"] == "exist":
                assert len(haha) == 1
            if httpParameters["checkDBType"] == "non-exist":
                assert haha == []