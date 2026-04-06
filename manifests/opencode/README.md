# OpenCode Kubernetes 部署

使用kind在本地部署opencode serve和web服务。

## 目录结构

```
opencode/
├── .env.example        # 环境变量模板
├── .gitignore          # 忽略 .env
├── k8s/
│   ├── kind-config.yaml    # kind集群配置
│   ├── opencode-serve.yaml # opencode serve部署配置
│   ├── opencode-web.yaml   # opencode web部署配置
│   ├── deploy.sh           # 部署脚本
│   ├── cleanup.sh          # 清理脚本
│   └── README.md           # 本文件
└── README.md               # 项目说明
```

## 前置要求

- Docker
- kind
- kubectl

## 快速部署

```bash
# 复制环境变量模板并修改
cp .env.example .env
vim .env

# 部署
cd k8s
./deploy.sh
```

密码优先级：`.env` 文件 > 环境变量 `OPENCODE_PASSWORD` > 交互式输入

## 访问服务

- **opencode serve**: http://localhost:5096
- **opencode web**: http://localhost:9090

## 配置说明

### 端口映射

| 服务 | 容器端口 | 主机端口 |
|------|----------|----------|
| opencode serve | 4096 | 5096 |
| opencode web | 8080 | 9090 |

### 数据持久化

数据存储在kind集群节点的 `/data/opencode` 目录，挂载到容器的 `/root/.local/share/opencode`。

## 清理

```bash
./cleanup.sh
```

## 相关文档

- [OpenCode Server 文档](https://opencode.ai/docs/server/)
- [OpenCode Web 文档](https://opencode.ai/docs/web/)
