# 部署
创建数据库
```
CREATE DATABASE xd26
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;
```

xd26_restart.sh
```shell
#! /bin/bash

DOCKER_CONTAINER_NAME="xd26"
DOCKER_TAG_NAME="$DOCKER_CONTAINER_NAME:0.0.1"
docker build -t $DOCKER_TAG_NAME --build-arg IP=172.31.188.191 .

docker stop $DOCKER_CONTAINER_NAME 2>/dev/null
docker rm $DOCKER_CONTAINER_NAME 2>/dev/null

docker run -d \
--name=$DOCKER_CONTAINER_NAME \
-v /root/logs/xd26_30010:/logs \
-p 30010:8080 \
-e "CONFIG_URL_SET_UP=http://172.31.188.191:23000/config/internal?key=xd26&cache=0" \
--restart=always \
$DOCKER_TAG_NAME
#  sleep 99999999

echo -e "\n\n\nsudo docker ps --filter \"name=$DOCKER_CONTAINER_NAME\"\n\n\n"
docker ps --filter "name=$DOCKER_CONTAINER_NAME"
echo -e "\n\n\n"; sleep 1; docker ps --filter "name=$DOCKER_CONTAINER_NAME"
```

# 使用
查询公开数据
```
curl 'http://localhost:30010/api/category/list' | jq .
```

# 本地
config.yml
```
LOG_PATH: "/Users/lijusheng/senyu/logs/config_server/app.log"
StaticPath: "/Users/lijusheng/codes/config_server/src/static"
```
pycharm 
```
设置src为 source root路径
python src/main/run.py

CONFIG_URL_SET_UP=http://192.168.3.67:23000/config/internal?key=xd26&cache=0
curl -X 'POST' \
  'http://localhost:23000/config/manage' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "key": "xd26",
  "value": {
      "ENV": "prod",
      "PORT": "8080",
      "LOG_PATH": "/logs/app.log",
      "LOG_LEVEL": "INFO",
      "REDIS_DSN": "redis://172.31.188.191:6379/0",
      "SERVER_NAME": "xd",
      "DATABASE_DSN": "mysql+aiomysql://root:root@172.31.188.191:3306/xd26",
      "SERVER_VERSION": "0.0.1",
      "SERVER_DESCRIPTION": "xd"
    },
  "name": "测试",
  "tag": "",
  "group_name": "internal",
  "type": 0
}' | jq .
```

# python环境
```
python=3.9.20
依赖包：统一 localhost:50000/us_base 里面的 requirements.txt
```
# 数据库
```
mysql：xd25
```
# run
```
设置环境变量


{
  "data": ,
  "code": 0,
  "msg": "ok"
}

放置文件：config.yml
LOG_PATH: "/Users/lijusheng/mywork/logs/algorithm_cra/log"
StaticPath: "/Users/lijusheng/sen_yu/python_codes/user_server/src/static"

设置src为 source root路径

执行
/Users/mac/mywork/code_py_venv/user_server/bin/python /Users/mac/python_codes/xd25_back/src/main/run.py

在第一次执行时，会加入一条数据：
/Jcheck/src/apps/domain/repositories/repo_biz.py
```

# 镜像制作并启动
```
./restart_168_jcheck.sh

#! /bin/bash
DOCKER_CONTAINER_NAME="j_check"
DOCKER_TAG_NAME="$DOCKER_CONTAINER_NAME:0.0.1"
docker build -t $DOCKER_TAG_NAME .

docker stop $DOCKER_CONTAINER_NAME 2>/dev/null
docker rm $DOCKER_CONTAINER_NAME 2>/dev/null

docker run -d \
--name=$DOCKER_CONTAINER_NAME \
-p 23030:8080 \
-v /root/data_log/jcheck:/logs \
-e "CONFIG_URL_SET_UP=http://192.168.3.67:23000/config/internal?key=jcheck" \
--restart=always \
$DOCKER_TAG_NAME
# sleep 99999999

echo -e "\n\n\nsudo docker ps --filter \"name=$DOCKER_CONTAINER_NAME\"\n\n\n"
docker ps --filter "name=$DOCKER_CONTAINER_NAME"
echo -e "\n\n\n"; sleep 2; docker ps --filter "name=$DOCKER_CONTAINER_NAME"
```

# 使用说明
```
前端调用1，2两个接口
后端调用 2号接口

1. 请求验证码
    请求：
    curl -X 'GET' \
    'http://192.168.3.67:23020/api/jcheck/j_img' \
    -H 'accept: application/json' \
    -H 'biz_code: 343775d016ae6475451be8d067f28b72' | jq .

    返回：
        正常：
        {
          "data": {
            "img64": "data:image/png;base64,iVBJg ...... gg==",
            "serial": "bb06f576-3b81-4f53-b316-74c562de9f1d"
          },
          "code": 0,
          "msg": "ok"
        }
        异常：
        {
          "msg": "biz_code 非法: adfasf ",
          "code": 1
        }
    参数说明：
        入参：
            biz_code：唯一业务标识码
        出参：
            img64： base64格式 图片
            serial： 流水号
     其他可配置：
         最大提交m次答案，最长在n分钟内提交（m、n可以根据业务配置），后端需要在x秒内验证
         默认是 前端：60秒内5次，后端120秒内去验证有效

2. 校验
    前端：
    curl  -X POST 'http://192.168.3.67:23020/api/jcheck/check' \
    -H 'Content-Type: application/json' \
      --data-raw '{"serial":"1eee85aa-dd8b-4a22-bbaf-db96a79b9434","result":"7423"}' | jq .

    验证通过：200
        {"msg":"ok","code":0}
    验证不通过: 200
        {"msg":"异常","code":-1}
    参数错误： 400
        {
          "message": "参数错误：形式错误",
          "errors": [
            {
              "loc": [
                "body",
                "serial"
              ],
              "msg": "field required",
              "type": "value_error.missing"
            }
          ],
          "code": 1,
          "msg": "非法入参"
        }

    后端：
    curl -X POST  'http://192.168.3.67:23020/api/jcheck/check' \
    -H 'Content-Type: application/json' \
      --data-raw '{"biz_code":"343775d016ae6475451be8d067f28b72","serial":"1eee85aa-dd8b-4a22-bbaf-db96a79b9434"}' | jq .
    结果同上

    参数说明：
        入参：
            biz_code：唯一业务标识码【后端需要】
            serial： 水流号    【前后端都需要】
            result： 输入的结果【前端需要】
        出参：
            code： 非零为异常
```


b. 配置接口
```
启动时，增加环境变量
CONFIG_URL_SET_UP=http://localhost:8001/config/gateway
内容：
{
    "SERVER_NAME": "api",
    "SERVER_VERSION": "0.0.1",
    "SERVER_DESCRIPTION": "统一网关",
    "ENV": "prod",
    "PORT": "8080",
    "LOG_LEVEL": "INFO",
    "LOG_PATH": "/logs/app.log",
    "CONFIG_URL": "http://192.168.3.67:8000/config_server/config/ad",
    "ProductStaticPath": "/app/static"
}
'''
'''
{
    "data": {
        "SERVER_NAME": "api",
        "SERVER_VERSION": "0.0.1",
        "SERVER_DESCRIPTION": "微服务统一网关gateway",
        "ENV": "prod",
        "PORT": "8080",
        "LOG_LEVEL": "INFO",
        "LOG_PATH": "/logs/app.log",
        "CONFIG_URL": f"http://{host}:8000/ad",
    }
}

CONFIG_URL
{
    "data": {
        "UserUrl": [f"http://{host}:8002/user/who", ],
        "ConfigUrl": [f"http://{host}:8000/ad", ],
        "user": {
            "urls": [f"http://{host}:8002/", ],
            "open_path": ["wechat/code_login", "user/who"],
            "path": {
            }
        }
    }
}
```
c. 用户服务
```
需要f"http://{host}:8002/user/who" 这个接口来将token换取用户信息
```

## 镜像制作并启动
```
./restart_docker_test.sh
./restart_docker_prod.sh
```

## 常用命令
```
手动刷新配置
curl http://localhost:8000/api/reload

curl http://localhost:8000/api/user/who -H 'token: e72b151c-0fc9-405a-b768-f9b846bd1ac5'   | jq .

http://localhost:8000/api/docs
```

在src同级目录下，vi config.yml，覆盖配置中心的配置信息
```
PORT: "8000"
LOG_PATH: "/Users/lijusheng/mywork/logs/algorithm_cra/log"
StaticPath: "/Users/lijusheng/sen_yu/python_codes/user_server/src/static"
```
