`【前提】进入到工程目录rg-interfaceAutoTest下`
### 方式一：使用runAll.py

```
python runAll.py {param01} {param02}
```

*  {param01}: 必传。表示需要执行的测试用例文件夹或文件（可传rg-interfaceAutoTest目录下的相对路径）
*  {param02}：可不传，默认为空。表示是否需要直接在默认浏览器中打开allure测试报告，需要则传参“open”；不需要则不需要传该参数
*  例如 : 
    * [ ] 执行所有测试用例并自动打开测试报告：python runAll.py ./ open 
    * [ ] 执行指定文件夹./testCase/linkid/domain下的所有测试用例：python runAll.py testCase/linkid/domain
    * [ ] 执行指定测试用例文件：python runAll.py testCase/linkid/domain/userController/findCategoryCode/test_findCategoryCode.py


### 方式二：使用pytest命令
```
pytest 文件夹或测试用例文件
```
