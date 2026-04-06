# Kind 本地部署

使用 kind 在本地部署 opencode serve 和 web 服务。

## 前置要求

- Docker
- kind
- kubectl

## 快速部署

```bash
./deploy.sh
```

密码优先级：`.env` 文件 > 环境变量 `OPENCODE_PASSWORD` > 交互式输入

## 访问服务

- **opencode serve**: http://localhost:5096
- **opencode web**: http://localhost:9090

## 清理

```bash
./cleanup.sh
```
