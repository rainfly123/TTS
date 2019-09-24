#!/usr/bin/env python
#coding:utf8
#pip install aliyun-python-sdk-core

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json
import requests

# 创建AcsClient实例
client = AcsClient(
   "TAI4FsbxG569MjGwRFZQBcJ",
   "uLvYiDlCjgHwAJ2WIfDtrzWxMNtHT",
   "cn-shanghai"
);
# 创建request，并设置参数
def getToken():
    request = CommonRequest()
    request.set_method('POST')
    request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
    request.set_version('2019-02-28')
    request.set_action_name('CreateToken')
    response = client.do_action_with_exception(request)
    res = json.loads(response)
    token = res['Token']['Id']
    return token



def GetTTS(male="female", text="Hello", en=False):
    url = 'https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts?spm=a2c4g.11186623.2.34.76315275VkLfUR'
    token = getToken()
    if male == "female":
        if en :
            role = "emily"
        else:
            role = "aiya"
    elif en :
        role = "eric"
    else:
        role = "aida"

    payload = {
    "appkey": "aQ4hvgaFONxt5aqs",
    "token": token,
    "text": text,
    "format": "mp3",
    "voice": role,
    "speech_rate": -100
    }

    r = requests.get(url, params=payload)
    if r.headers['Content-Type'] == "audio/mpeg":
        return r.content

if __name__ == "__main__":
    print getTTS()
