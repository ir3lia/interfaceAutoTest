import json
import requests


# url:swagger接口ip+端口号，如：172.17.8.122:8901
# callSuff：接口请求url后半部分，比如：/linkid/api/aggregate/user/pageQueryUsers
# httpType：接口http协议类型，如：POST,GET,DELETE,PUT
# parame：接口josn参数
# UserHeader:sourceid中一般需要授权的接口使用
# token：Bearer token
def httpRequests(url, callSuff, httpType, parame='', UserHeader='5c7776dfedd9a9952b3b44c2', token=''):
    requrl = url + callSuff
    headers = {'Content-Type': 'application/json', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'Authorization': "Bearer " + token, 'User-Header': UserHeader}
    req = ''
    httpType = httpType
    if httpType == "POST":
        if parame != '':
            req = requests.post(url=requrl, headers=headers, data=json.dumps(parame))  # 生成页面请求的完整数据
        elif parame == '':
            req = requests.post(url=requrl, headers=headers)  # 生成页面请求的完整数据
    elif httpType == "GET":
        if parame != '':
            req = requests.get(url=requrl, headers=headers, data=json.dumps(parame))  # 生成页面请求的完整数据
        elif parame == '':
            req = requests.get(url=requrl, headers=headers)  # 生成页面请求的完整数据
    elif httpType == "DELETE":
        if parame != '':
            req = requests.delete(url=requrl, headers=headers, data=json.dumps(parame))  # 生成页面请求的完整数据
        elif parame == '':
            req = requests.delete(url=requrl, headers=headers)  # 生成页面请求的完整数据
    elif httpType == "PUT":
        if parame != '':
            req = requests.put(url=requrl, headers=headers, data=json.dumps(parame))  # 生成页面请求的完整数据
        elif parame == '':
            req = requests.put(url=requrl, headers=headers)  # 生成页面请求的完整数据
    return req.json()

# POST协议上传文件接口
def UploadFile(url, callSuff, fileName, filePath, user):
    requrl = 'http://' + url + callSuff
    filePath = filePath.decode("utf-8")
    fileName = fileName.decode("utf-8")
    files = [('file', (fileName, open(filePath, 'rb'), 'application/vnd.ms-excel', {'Expires': '0'}))]
    headers = {'Conteny-Type': 'multipart/form-data', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'User-Header': user}
    res = requests.post(url=requrl, headers=headers, files=files)
    return res.json()

if __name__ == '__main__':
    #httpRequests("172.17.8.114:38901","/linkid/api/organization/all/organization","GET",UserHeader="5c7776dfedd9a9952b3b44c2")
    #prm = ["5ebe024586aeaa0006d691e1"]
    #headers = {'Content-Type': 'application/json', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'User-Header': '5c7776dfedd9a9952b3b44c2'}
    #req = requests.post(url="http://172.17.8.166:30901/linkid/api/user/find/category/code/objectId", headers=headers, data=json.dumps(prm))
    #print(req.json())
    req1 = httpRequests("http://172.17.8.242:9888", "/nodeManager/software/delSoftwareInfo/11111", "DELETE")
    req2 = httpRequests("http://172.17.8.242:9888", "/nodeManager/software/delSoftwareInfo/5ef1b78673ec7d00060a79e1", "DELETE")
    print(req1)
    print(req2)

