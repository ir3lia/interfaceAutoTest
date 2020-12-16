#-*-coding=utf-8-*-
import os
import codecs
import configparser
import sys

porDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(porDir, "linkid_config.ini")
root_path = os.path.abspath(os.path.dirname(porDir) + os.path.sep + ".")
sys.path.append(root_path)

class linkid_ReadConfig():
    def __init__(self):
        fd = open(configPath, encoding="utf-8")
        data = fd.read()
        #rmove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath, encoding="utf-8")

    def get_url(self, name):
        value = self.cf.get("PATH", name)
        return value