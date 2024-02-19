import os
import urllib.parse
import urllib.request




def sc_send(text, desp='', channel=98, key='SCT170695TVgILvV5PXeNF7akHCyhT8V7d'):
    postdata = urllib.parse.urlencode({'text': text, 'desp': desp, 'channel': channel}).encode('utf-8')
    url = f'https://sctapi.ftqq.com/{key}.send'
    req = urllib.request.Request(url, data=postdata, method='POST')
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
    return result

