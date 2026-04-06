#!/bin/bash
set -e

# 删除部署
kubectl delete -f opencode-serve.yaml --ignore-not-found
kubectl delete -f opencode-web.yaml --ignore-not-found
kubectl delete secret opencode-secret --ignore-not-found

# 删除kind集群
kind delete cluster --name opencode

# 清理数据目录
sudo rm -rf /data/opencode

echo "清理完成！"
