import yaml

def get_test_data(test_data_path):
    case = []  # 存储测试用例名称
    http = []  # 存储请求对象
    expected = []  # 存储预期结果
    with open(test_data_path) as f:
        dat = yaml.load(f.read(), Loader=yaml.SafeLoader)
        test = dat['tests']
        for td in test:
            case.append(td.get('case', ''))
            http.append(td.get('http', {}))
            expected.append(td.get('expected', {}))
    parameters = zip(case,http, expected)
    return case, parameters

def get_config(test_host_path,type):
    configs = []  # 存储预期结果
    with open(test_host_path) as f:
        dat = yaml.load(f.read(), Loader=yaml.SafeLoader)
        config = dat['config']
        for td in config:
            configs.append(td.get(type, {}))
    return configs

def get_apiPath(test_api_path):
    apipaths = []  # 存储预期结果
    with open(test_api_path) as f:
        dat = yaml.load(f.read(), Loader=yaml.SafeLoader)
        apiPath = dat['apiPath']
        for td in apiPath:
            apipaths.append(td.get('paths', {}))
    return apipaths