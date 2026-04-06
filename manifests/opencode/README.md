# OpenCode 部署配置

## 目录结构

```
opencode/
├── k8s/               # kind 本地部署（实验用）
├── fass/             # 阿里云 FC 部署
└── README.md
```

## 部署方式

### 阿里云 FC（生产环境）

```bash
cd fc
cp .env.example .env
vim .env
./deploy.sh
```

### Kind 本地实验

```bash
cd k8s
./deploy.sh
```

## 相关文档

- [OpenCode Server 文档](https://opencode.ai/docs/server/)
- [OpenCode Web 文档](https://opencode.ai/docs/web/)
