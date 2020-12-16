import pytest
import os
import sys
import shutil
if __name__ == '__main__':
    #清除之前的测试报告
    shutil.rmtree('result/allure-result/',ignore_errors=True)
    #执行测试用例
    pytest.main(['testCase/SMP/authentication/', "--alluredir", "result/allure-result"])
    #将历史执行结果文件替换到allure-result目录下，在测试报告中可以生成历史趋势图
    shutil.move("result/allure-report/history", "result/allure-result/history")
    # 执行命令，生成Allure测试报告
    split = 'allure ' + 'generate ' + 'result/allure-result ' + '-o ' + 'result/allure-report ' + '--clean'
    os.system(split)
    # 自动将生成的Allure测试报告在默认浏览器中打开
    os.system("allure open result/allure-report")