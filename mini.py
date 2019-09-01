import requests

APPID = 'wx1751282640de8bb1'
SECRET = 'adedb4ebc4680183061bc67d4ef6526e'


def get_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(APPID,
                                                                                                           SECRET)
    respon = requests.get(url)
    content = respon.content

    content = content.decode('utf-8')
    import json
    data = json.loads(content)
    access_token = data.get("access_token")
    return access_token


def getWXACode(classid, token):
    id = str(classid)
    # print("classid="+str(classid))
    # print("token="+token)
    if not token:
        print("token为空")
    else:
        url = 'https://api.weixin.qq.com/wxa/getwxacode?access_token={}'.format(token)
        data = {
            "path": "pages/lab/apply/apply?classid={}".format(classid),  # todo 传参
            # "path": "pages/lab/apply/apply?classid=10001",  # todo 传参
            "width": 1280,
            "auto_color": False,
            "line_color": {"r": 16, "g": 111, "b": 163},  # 自定义颜色 auto_color 为 false 时生效
            # "line_color": {"r": 233, "g": 195, "b": 65},  # 自定义颜色
            "is_hyaline": True  # 是否需要透明底色
        }

        # todo 不能使用data 要使用json
        ret = requests.post(url, json=data)
        with open(id + '.png', 'wb') as f:
            f.write(ret.content)
            print("生成:" + id)


def aotic():
    token = get_token()
    # for i in range(10090, 100091):
    getWXACode(10242, token)


aotic()
