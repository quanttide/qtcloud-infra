#!/bin/bash
set -e

REGION="${ALIYUN_REGION:-cn-hangzhou}"
BILLING_PERIOD="${1:-$(date -d 'last month' +%Y-%m)}"

echo "=== 阿里云账单查询 ==="
echo "计费周期: $BILLING_PERIOD"
echo ""

echo "--- 账号级账单 ---"
aliyun bssapi QueryBillOverviewBill \
  --BillingCycle "$BILLING_PERIOD" \
  --Granularity MONTHLY \
  2>/dev/null | jq '.' || echo "无法获取账单概览"
echo ""

echo "--- 详细账单 ---"
aliyun bssapi QueryBillList \
  --BillingCycle "$BILLING_PERIOD" \
  --Granularity MONTHLY \
  --MaxResults 100 \
  2>/dev/null | jq '.' || echo "无法获取详细账单"
echo ""

echo "--- 函数计算 (FC) 账单 ---"
aliyun bssapi QueryBillDetail \
  --BillingCycle "$BILLING_PERIOD" \
  --ProductCode fc \
  2>/dev/null | jq '.' || echo "无法获取 FC 账单"
echo ""

echo "--- 账单概览 ---"
aliyun bssapi GetBillOverview \
  --BillingCycle "$BILLING_PERIOD" \
  2>/dev/null | jq '.' || echo "无法获取账单概览"
