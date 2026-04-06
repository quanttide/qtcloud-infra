#!/bin/bash
set -e

# 配置
OPENCODE_VERSION="v1.2.27"
CLUSTER_NAME="opencode"

# 加载 .env 文件
if [ -f ../.env ]; then
    export $(grep -v '^#' ../.env | xargs)
elif [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# 获取密码
if [ -z "$OPENCODE_PASSWORD" ]; then
    read -sp "请输入 OpenCode 密码: " OPENCODE_PASSWORD
    echo
fi
if [ -z "$OPENCODE_PASSWORD" ]; then
    echo "错误：密码不能为空"
    exit 1
fi

# 创建kind集群（如果不存在）
if ! kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
    echo "创建kind集群 ${CLUSTER_NAME}..."
    kind create cluster --name ${CLUSTER_NAME} --config kind-config.yaml
else
    echo "kind集群 ${CLUSTER_NAME} 已存在"
fi

# 下载musl版本的opencode
echo "下载opencode ${OPENCODE_VERSION}..."
curl -fsSL -o /tmp/opencode-linux-x64-musl.tar.gz https://github.com/anomalyco/opencode/releases/download/${OPENCODE_VERSION}/opencode-linux-x64-musl.tar.gz
tar -xzf /tmp/opencode-linux-x64-musl.tar.gz -C /tmp/

# 复制opencode到kind集群节点
echo "复制opencode到kind集群节点..."
docker cp /tmp/opencode opencode-control-plane:/usr/local/bin/opencode
docker exec opencode-control-plane chmod +x /usr/local/bin/opencode

# 创建Secret
echo "创建Secret..."
kubectl delete secret opencode-secret --ignore-not-found
kubectl create secret generic opencode-secret --from-literal=password="${OPENCODE_PASSWORD}"

# 部署opencode serve
echo "部署opencode serve..."
kubectl apply -f opencode-serve.yaml

# 部署opencode web
echo "部署opencode web..."
kubectl apply -f opencode-web.yaml

# 等待pod启动
echo "等待pod启动..."
kubectl wait --for=condition=ready pod -l app=opencode-serve --timeout=300s
kubectl wait --for=condition=ready pod -l app=opencode-web --timeout=300s

# 显示服务状态
echo "部署完成！"
echo "opencode serve: http://localhost:5096"
echo "opencode web: http://localhost:9090"
echo ""
echo "Pod状态:"
kubectl get pods
echo ""
echo "服务状态:"
kubectl get svc
