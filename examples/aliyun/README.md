# 阿里云账单查询

使用阿里云 CLI 获取账号级账单信息，默认看上个月。

## 前提条件

```bash
pip install requests
aliyun configure
```

## 使用方法

### Shell

```bash
./aliyun-billing.sh                    # 查询上个月
./aliyun-billing.sh 2026-03            # 查询指定月份
```

### Python

```bash
python aliyun-billing.py               # 查询上个月
python aliyun-billing.py --period 2026-03
```
