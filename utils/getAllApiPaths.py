import os
import sys
o_path = os.getcwd()  #返回当前工作目录
sys.path.append(o_path)  #添加自己指定的搜索路径
from utils import readYaml
linkidApiPaths = readYaml.get_apiPath("../common/apiPaths/linkidPath.yaml")
ssoApiPaths = readYaml.get_apiPath("../common/apiPaths/ssoPath.yaml")
authenticationApiPaths = readYaml.get_apiPath("../common/apiPaths/authenticationPath.yaml")


def getJsonKeyValue(data):
    dataKey = []
    dataValue = []
    if isinstance(data, dict):
        for key in data:
            dataKey.append(key)
            dataValue.append(data[key])
    return dataValue


linkidPas = getJsonKeyValue(linkidApiPaths[0])
ssoPas = getJsonKeyValue(ssoApiPaths[0])
authenticationPas = getJsonKeyValue(authenticationApiPaths[0])

print(linkidPas, '\n -------以上是linkid所有api的path，以下是sso的所有api的path \n',ssoPas,authenticationPas)