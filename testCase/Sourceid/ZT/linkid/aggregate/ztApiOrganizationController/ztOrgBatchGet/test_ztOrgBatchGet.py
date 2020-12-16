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
from utils import readConfig
from utils import readYaml
from utils import jsonRead
from utils import zt_linkidApi
from utils import jsonAnalysis
from utils import mongoDataOpr
from utils import httpApi
from utils import checkConnect

testerName = 'yangxi'
controllerName = "ztApiOrganizationController"
interfaceChName = "批量查询组织"
interfaceEnName = "batchGetOrg"



commonConfig = readYaml.get_config("common/config.yaml","common")
linkidApiPaths = readYaml.get_apiPath("common/apiPaths/linkidPath.yaml")
ssoApiPaths = readYaml.get_apiPath("common/apiPaths/ssoPath.yaml")
tokenJ = zt_linkidApi.accessToken(commonConfig[0]['sid'], ssoApiPaths[0]['tokenPath'],commonConfig[0]['appId'],commonConfig[0]['appSecret'])
urlIP = commonConfig[0]["sidself"]
urlPath = linkidApiPaths[0]['publicZtOrgGetPath']

dirPath, fileName = os.path.split(os.path.abspath(__file__))
cases_main,parameters_main = jsonRead.loadHttpData(dirPath + "/testData.json",'mainCaseData')
cases_all,parameters_all = jsonRead.loadHttpData(dirPath + "/testData.json",'allCaseData')
dbJsonPath = dirPath + "/dbData.json"
dbName = "linkid"

def setup_module():
    if checkConnect.checkConnection(urlIP) == 'error': 
        raise Exception("服务器访问失败，请确定环境是否正常！")

@allure.epic(controllerName)
@allure.feature(interfaceChName)
class Test_class():
    def setup_class(self):
        print("====（整个测试类）前置条件：插入组织数据====")
        mongoDataOpr.oprDatasToDB(dbJsonPath,dbName,"insert")

    def teardown_class(self):
        print("\n ====（整个测试类）后置条件：清理数据库====")
        mongoDataOpr.oprDatasToDB(dbJsonPath,dbName,"delete")

    @allure.story(interfaceChName + "-主流程")
    @allure.title("{case}")
    @pytest.mark.dependency(name=interfaceEnName + "_main")
    @pytest.mark.parametrize("case,description,httpParameters", list(parameters_main))
    def test_main(self, case,description, httpParameters):
        allure.attach('{0}'.format(testerName),"测试人员")
        allure.attach(json.dumps(httpParameters["query"],ensure_ascii=False),"接口入参",allure.attachment_type.JSON)  #测试用例的入参
        if httpParameters["paramType"] == "string":
            stringParams = jsonAnalysis.getStringParams(httpParameters["query"])
            urlPath2 = urlPath + stringParams
            postJ = httpApi.httpRequests(urlIP,urlPath2,httpParameters["httpType"],token=tokenJ['access_token'])
        elif httpParameters["paramType"] == "json":
            postJ = httpApi.httpRequests(urlIP,urlPath,httpParameters["httpType"],parame=httpParameters["query"],token=tokenJ['access_token'])
        else:
            assert 0 , '参数类型「'+httpParameters["paramType"]+'」无法处理！'
        allure.attach(json.dumps(postJ,ensure_ascii=False),"接口出参",allure.attachment_type.JSON)  #测试用例的出参
        keyPaths = jsonAnalysis.getKeyPaths(httpParameters["response"])
        for path in keyPaths:
            res1 = jsonAnalysis.getKeyValues(httpParameters["response"],path)
            res2 = jsonAnalysis.getKeyValues(postJ,path)
            assert len(res2) > 0 , path + "不存在"
            assert res1 == res2 , path + " 值错误！"
        if httpParameters["isCheckDB"]:
            haha = mongoDataOpr.oprDatasToDB(dbJsonPath,dbName,"find")
            if httpParameters["checkDBType"] == "exist":
                assert len(haha) == 1
            if httpParameters["checkDBType"] == "non-exist":
                assert haha == []

    @allure.title("{case}")
    @allure.story(interfaceChName + "-测试用例")
    @pytest.mark.dependency(name=interfaceEnName + "_all", depends=[interfaceEnName + "_main"])
    @pytest.mark.parametrize("case,description,httpParameters", list(parameters_all))
    def test_all(self,case,description,httpParameters):
        allure.attach('{0}'.format(testerName),"测试人员")
        allure.attach(json.dumps(httpParameters["query"],ensure_ascii=False),"接口入参",allure.attachment_type.JSON)  #测试用例的入参
        if httpParameters["paramType"] == "string":
            stringParams = jsonAnalysis.getStringParams(httpParameters["query"])
            urlPath2 = urlPath + stringParams
            postJ = httpApi.httpRequests(urlIP,urlPath2,httpParameters["httpType"],token=tokenJ['access_token'])
        elif httpParameters["paramType"] == "json":
            postJ = httpApi.httpRequests(urlIP,urlPath,httpParameters["httpType"],parame=httpParameters["query"],token=tokenJ['access_token'])
        else:
            assert 0 , '参数类型「'+httpParameters["paramType"]+'」无法处理！'
        allure.attach(json.dumps(postJ,ensure_ascii=False),"接口出参",allure.attachment_type.JSON)  #测试用例的出参
        keyPaths = jsonAnalysis.getKeyPaths(httpParameters['response'])
        for path in keyPaths:
            res1 = jsonAnalysis.getKeyValues(httpParameters["response"],path)
            res2 = jsonAnalysis.getKeyValues(postJ,path)
            assert len(res2) > 0 , path + "不存在"
            assert res1 == res2 , path + " 值错误！"
        if httpParameters["isCheckDB"]:
            haha = mongoDataOpr.oprDatasToDB(dbJsonPath,dbName,"find")
            if httpParameters["checkDBType"] == "exist":
                assert len(haha) == 1
            if httpParameters["checkDBType"] == "non-exist":
                assert haha == []
                

