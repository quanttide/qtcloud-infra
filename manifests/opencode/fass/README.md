# 阿里云 FC 部署配置

## 前置要求

- Docker
- Fun 工具 (`npm install @alicloud/fun -g`)
- 阿里云账号配置 (`fun config`)

## 快速部署

```bash
cd fc

# 配置环境变量
cp .env.example .env
vim .env

# 部署
./deploy.sh
```

## 架构说明

- **opencode-serve**: AI 对话服务
- **opencode-web**: Web UI 服务

## 持久化存储

使用 NAS 挂载 `/root/.local/share/opencode` 目录保存配置和会话数据。

## 注意事项

1. 需要先创建 VPC、VSwitch、安全组
2. 需要创建 NAS 文件系统并添加挂载点
3. 需要创建容器镜像服务命名空间和仓库
