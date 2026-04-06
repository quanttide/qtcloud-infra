#!/bin/bash
set -e

source .env

echo "构建 Docker 镜像..."
docker build -t opencode:latest .

echo "推送镜像到阿里云容器镜像服务..."
docker tag opencode:latest ${REGION}.cr.aliyuncs.com/${IMAGE_NAMESPACE}/opencode:latest
docker push ${REGION}.cr.aliyuncs.com/${IMAGE_NAMESPACE}/opencode:latest

echo "部署到阿里云FC..."
fun deploy -y

echo "部署完成！"
echo "查看服务: https://fc.console.aliyun.com/fc"
