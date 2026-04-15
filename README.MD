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
-v /root/static/xd26/30010:/app/static \
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
      "ProductStaticPath": "/app/static",
      "LOG_LEVEL": "INFO",
      "REDIS_DSN": "redis://172.31.188.191:6379/0",
      "SERVER_NAME": "xd",
      "DATABASE_DSN": "mysql+aiomysql://root:root@172.31.188.191:3306/xd26",
      "SERVER_VERSION": "0.0.1", "MP_APPID": "", "MP_SECRET": "",
      "SERVER_DESCRIPTION": "xd"
    },
  "name": "测试",
  "tag": "",
  "group_name": "internal",
  "type": 0
}' | jq .
```
