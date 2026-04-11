#! /bin/bash
HOST="192.168.1.64"
DOCKER_CONTAINER_NAME="zichan"
DOCKER_TAG_NAME="$DOCKER_CONTAINER_NAME:0.0.1"
docker build -t $DOCKER_TAG_NAME --build-arg IP=$HOST .

docker stop $DOCKER_CONTAINER_NAME 2>/dev/null
docker rm $DOCKER_CONTAINER_NAME 2>/dev/null

docker run -d \
--name=$DOCKER_CONTAINER_NAME \
-p 23090:8080 \
-v /root/data_log/zichan:/logs \
-e "CONFIG_URL_SET_UP=http://192.168.3.67:23000/config/internal?key=zichan&cache=0" \
--restart=always \
$DOCKER_TAG_NAME
# sleep 99999999

echo -e "\n\n\nsudo docker ps --filter \"name=$DOCKER_CONTAINER_NAME\"\n\n\n"
docker ps --filter "name=$DOCKER_CONTAINER_NAME"
echo -e "\n\n\n"; sleep 1; docker ps --filter "name=$DOCKER_CONTAINER_NAME"
