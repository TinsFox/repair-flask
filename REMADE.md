# 课室维护
### 目的：快速、高效上报课室、多媒体设备故障
A1:报修人联系方式：首次手动填写，第二次自动填充
A2:与课室管理对接问题。遇到无法马上解决的问题，影响上课时，由跟进人员直接建议课室管理员提出更换教室
A3:备注方面。考虑到教室网络问题，上传图片对网络的要求比较高，并且我们认为这会增加报修的繁琐性了，所以是不建议让报修人上传图片的。当然，确实是要的话技术上可以实现，具体使用还要看使用效果
A4:课室号填充：方式一：扫描二维码自动填充；方式二：手动选择



# Python 文档
baseUrl:`http://10.3.35.220:5000/v1`
## 小程序登录
url:`/client/mini`
methods:POST
param:
``` json
{
    "code":"*",
    "userInfo":""
}
```

return:
``` json
{
    "data":{
        "error_code": 0
        "msg": "ok"
        "request": "POST /v1/client/mini"}
}
```

## 小程序下单
url:`/order/add`
methods:POST
param:

``` json
{
    "code":"*",
    "roomid":"课室 A1-201",
    "content":"故障描述",
    "equipment":"设备类型",
    "phone":"电话(选填)",
}
```

return:
``` json
{
    "data":{
        "error_code": 0
        "msg": "报修成功"
        "request": "POST /v1/order/add"
        }
}
```

# H5
全局声明：管理员的所有操作都需要在Authorization 中 Basic Auth 带上token， token放在Username中，Password为空

## 管理员登录
url:`/token`
methods:POST
param:

```  json
{
    "account":"999@qq.com",
    "secret":"123456",
    "type":100（默认写死100，int类型）
}
```

return:

```  json
{
    "data": {
        "list": [
            {
                "expiration": 2592000,
                "token": "eyJhbGciOiJIU"
            }
        ]
    },
    "errcode": 0,
    "msg": "登录成功"
}
```

## 获取所有未接订单
url:`/order/list`
methods:get
param: token

``` json
{
    "data": {
        "list": [
            {
                "content": "2223",
                "equipment": "5243",
                "id": "04048aeca2c0f5d84639358008ed2ae7",
                "phone": "13924387832",
                "roomid": "A2-131",
                "status": 1,
                "uuid": null
            },
            {
                "content": "救命3",
                "equipment": "笔记本",
                "id": "7674eb617ad36fd4caa908fdf541eb47",
                "phone": "13924387832",
                "roomid": "A2-131",
                "status": 1,
                "uuid": null
            }
        ]
    },
    "errcode": 0,
    "msg": "获取成功"
}
```


## 接单
url:`/order/accept`
methods:patch

param:toekn

```  json
{
    "id":"9fe1951b42557d0a1e6a2896e065d56e"//订单的id
	
}
```

return:

```  json
{
    "error_code": 0,
    "msg": "接单成功",
    "request": "PATCH /v1/order/accept"
}
```
## 完成订单
url:`/order/finsh`
methods:patch

param:toekn

```  json
{
    "id":"9fe1951b42557d0a1e6a2896e065d56e"//订单的id
	
}
```

return:

```  json
{
    "error_code": 0,
    "msg": "订单完成",
    "request": "PATCH /v1/order/finsh"
}
```
## 我的未完成订单列表

url:`/order/mylist`
methods:get

param:toekn

```  json
{
    
}
```

return:

```  json
{
    "data": {
        "list": []
    },
    "errcode": 0,
    "msg": "未完成订单列表"
}
```


## 我的已完成订单

url:`/order/myfinsh`
methods:get

param:toekn

```  json
{
    
}
```

return:

```  json
{
    "data": {
        "list": [
            {
                "content": "救命",
                "equipment": "电脑",
                "id": "9fe1951b42557d0a1e6a2896e065d56e",
                "phone": "13924387832",
                "roomid": "A2-131",
                "status": 4,
                "uuid": "2"
            }
        ]
    },
    "errcode": 0,
    "msg": "已完成订单列表"
}
```


## 他人订单

url:`/order/other`
methods:get

param:toekn

```  json
{
    
}
```

return:

```  json
{
    "data": {
        "list": [
            {
                "content": "救命2",
                "equipment": "笔记本",
                "id": "a3522fb1fd813afb4daa843f0d4eebed",
                "phone": "13924387832",
                "roomid": "A2-131",
                "status": 0,
                "uuid": "5"
            }
        ]
    },
    "errcode": 0,
    "msg": "他人订单"
}
```