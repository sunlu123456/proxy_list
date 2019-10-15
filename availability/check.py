# -*- coding: UTF-8 -*-
import time
import json
import config
import requests


def crawl_handle(protocal, proxy, queue_persistence):
    if protocal is 'http':
        http, h_anonymity, h_interval = connect('http://httpbin.org/get', proxy)
        if http:
            proxy['protocol'] = 'http'
            proxy['anonymity'] = h_anonymity
            proxy['speed'] = h_interval
            queue_persistence.put(proxy)
            # config.console_log('验证通过的 http 代理: ' + json.dumps(proxy, ensure_ascii=False), 'green')
        else:
            # config.console_log('无效的 http 代理: ' + json.dumps(proxy, ensure_ascii=False), 'red')
            pass

    elif protocal is 'https':
        https, hs_anonymity, hs_interval = connect('https://httpbin.org/get', proxy)
        if https:
            proxy['protocol'] = 'https'
            proxy['anonymity'] = hs_anonymity
            proxy['speed'] = hs_interval
            queue_persistence.put(proxy)
            # config.console_log('验证通过的 https 代理: ' + json.dumps(proxy, ensure_ascii=False), 'green')
        else:
            # config.console_log('无效的https代理: ' + json.dumps(proxy, ensure_ascii=False), 'red')
            pass


def store_handle(protocal, proxy, persister):
    if protocal is 'http':
        http, h_anonymity, h_interval = connect('http://httpbin.org/get', proxy)
        if http:
            proxy['speed'] = h_interval
            persister.update(proxy)
        else:
            persister.delete(proxy)
    elif protocal is 'https':
        https, hs_anonymity, hs_interval = connect('https://httpbin.org/get', proxy)
        if https:
            proxy['speed'] = hs_interval
            persister.update(proxy)
        else:
            persister.delete(proxy)


@config.catch_exception_logging(None)
def connect(url, proxy):
    try:
        start_point = time.time()
        response = requests.get(url, proxies={
            'http': 'http://%s:%s' % (proxy['ip'], proxy['port']),
            'https': 'http://%s:%s' % (proxy['ip'], proxy['port'])
        }, **{'timeout': 30, 'headers': config.get_http_header()})
        if response.ok:
            interval = round(time.time() - start_point, 2)
            res_json = json.loads(response.text)
            ip = res_json['origin']
            if ',' in ip:
                anonymity = 'transparent'
            else:
                anonymity = 'anonymous'
            return True, anonymity, interval
        else:
            return False, False, False
    except (Exception,):
        return False, False, False


if __name__ == '__main__':
    proxy = {'ip': '27.43.189.210', 'port': '9999'}
    http, h_anonymity, h_interval = connect('http://httpbin.org/get', proxy)
    print(h_anonymity)
