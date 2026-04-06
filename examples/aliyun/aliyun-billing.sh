#!/bin/bash
set -e

REGION="${ALIYUN_REGION:-cn-hangzhou}"
BILLING_PERIOD="${1:-$(date -d 'last month' +%Y-%m)}"

echo "=== 阿里云账单查询 ==="
echo "计费周期: $BILLING_PERIOD"
echo "区域: $REGION"
echo ""

echo "--- 实例账单 ---"
aliyun bssopenapi describe-instance-bill \
  --billing-cycle "$BILLING_PERIOD" \
  --granularity MONTHLY \
  2>&1 | jq '.'
echo ""

echo "--- 分账账单 ---"
aliyun bssopenapi describe-split-item-bill \
  --billing-cycle "$BILLING_PERIOD" \
  2>&1 | jq '.'
echo ""

echo "--- 账户余额 ---"
aliyun bssopenapi query-account-balance 2>&1 | jq '.'