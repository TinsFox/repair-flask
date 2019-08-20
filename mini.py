"""
    Created by  on 2019-08-19.
"""

__author__ = 'TinsFox'

import urllib.request
import urllib.parse
import json

appid = 'wx1751282640de8bb1'
appsecret = 'adedb4ebc4680183061bc67d4ef6526e'


# 获取TOKEN
def getToken(appid, appsecret):
    # 这个是微信获取小程序码的接口
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}'.format(
        appid=appid, appsecret=appsecret)
    # 准备一下头
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    }

    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    readData = response.read()
    readData = readData.decode('utf-8')
    obj = json.loads(readData)
    print(obj)
    print(obj['access_token'])
    return obj['access_token']


# 获取小程序码
def getACodeImage(token, file):
    # 这个是微信获取小程序码的接口
    url = 'https://api.weixin.qq.com/wxa/getwxacode?access_token={token}'.format(token=token)
    # 准备一下头
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    }
    # 用Post传值，这里值用JSON的形式
    path = "pages/lab/apply/apply?classid=file".format(file=file)
    values = {"path": path,
              "width": 430
              }
    # 将字典格式化成能用的形式,urlencode不能用
    # data = urllib.parse.urlencode(values).encode('utf-8')
    # 使用json.dumps的方式序列化为字符串，然后bytes进行编码
    data = json.dumps(values)
    data = bytes(data, 'utf8')
    # 创建一个request,放入我们的地址、数据、头
    request = urllib.request.Request(url, data, headers)
    # 将获取的数据存在本地文件
    readData = urllib.request.urlopen(request).read()
    f = open(file, "wb")
    f.write(readData)
    f.close()


def automatic(token):
    for i in range(1, 4):
        name = str(i) + '.jpg'
        print(name)
        # imageName = 1001 + 1
        getACodeImage(token, name)


token = getToken(appid, appsecret)
# getACodeImage(token, 'wxCode.jpg')
automatic(token)
