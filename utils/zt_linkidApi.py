#coding=utf-8
import json
import requests

def accessToken(sourceidURL, callSuff,clientId,clientSecret):
    url = sourceidURL + callSuff
    data={'grant_type':'client_credentials','client_id':clientId,'client_secret':clientSecret}
    response = requests.request("GET", url,params=data)
    j = json.loads(response.text)
    return j


def batchGetOrg(sourceidURL, callSuff , accessToken, params):
    url = sourceidURL + callSuff
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + accessToken
    }
    response = requests.request("POST", url,data=json.dumps(params), headers=headers)
    j = json.loads(response.text)
    return j

def postApi(sourceidURL, callSuff , params):
    url = sourceidURL + callSuff
    headers = {
        'Content-Type': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Header': '5c7776dfedd9a9952b3b44c2'
    }
    response = requests.request("POST", url,data=json.dumps(params,ensure_ascii=False).encode('utf-8'), headers=headers)
    j = json.loads(response.text)
    return j