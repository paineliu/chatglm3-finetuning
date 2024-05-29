from time import sleep
import requests
import json

def jss_post(ip, port, path, query):
    url = 'http://%s:%s/%s' % (ip, port, path)
    print(url)
    try:
        r = requests.post(url=url, data=query)
        return r.text
    except:
        return ""
    
def test(ip, port):
    
    query_json = {}
    query_json['userName'] = 'blcu'
    ret = jss_post(ip, port, 'getToken', json.dumps(query_json))
    print(ret)
    ret = json.loads(ret)
    query_json = {}
    query_json['token'] = ret['data']
    query_json['messages'] = [{'content':'文化','role':'user'}]
    ret = jss_post(ip, port, 'chat', json.dumps(query_json))
    print(ret)
    print()


if __name__ == "__main__":
    test('202.112.194.54', '8102')
    # test('127.0.0.1', '8102')
