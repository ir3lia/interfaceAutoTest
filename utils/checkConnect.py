import requests

def checkConnection(url):
    try:
        ret = requests.get(url, timeout=1)
        return ret.status_code
    except Exception as e:
        return "error"