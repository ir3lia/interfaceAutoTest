#-*-coding=utf-8-*-

import configparser
from configparser import ConfigParser

def getIniValue(path,item,name):
    cfg = ConfigParser()
    cfg.read(path)
    value = ''
    try :
        value = cfg.get(item, name)
    except Exception as e:
        print(str(e))
    return value

#mongoIp = getIniValue('../common/config.ini',"DATABASE","mongodbIp")
#usersSavePath = getIniValue('../common/apiPaths/linkid.ini',"PATH","publicZtOrgList")
#print(mongoIp,usersSavePath)

