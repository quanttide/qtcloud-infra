#!/bin/bash
set -e

REGION="${ALIYUN_REGION:-cn-hangzhou}"
BILLING_PERIOD="${1:-$(date -d 'last month' +%Y-%m)}"

echo "=== 阿里云账单查询 ==="
echo "计费周期: $BILLING_PERIOD"
echo "区域: $REGION"
echo ""

BILL_DATA=$(aliyun bssopenapi describe-instance-bill \
  --billing-cycle "$BILLING_PERIOD" \
  --granularity MONTHLY \
  2>&1)

echo "--- 账单汇总 ---"
echo "$BILL_DATA" | jq -r '
  .Data.Items | 
  group_by(.ProductName) | 
  map({
    product: .[0].ProductName,
    total: ([.[].PretaxAmount] | add | . * 100 | floor / 100)
  }) | 
  sort_by(-.total) |
  .[] | 
  "  \(.product): ¥\(.total)"
'

TOTAL=$(echo "$BILL_DATA" | jq -r '
  [.Data.Items[] | select(.Item == "PayAsYouGoBill") | .PretaxAmount] | 
  add | 
  . * 100 | floor / 100
')

echo ""
echo "--- 总计 ---"
echo "  ¥$TOTAL"
echo ""

echo "--- 账户余额 ---"
aliyun bssopenapi query-account-balance 2>&1 | jq -r '
  "  可用余额: ¥\(.Data.AvailableAmount) \(.Data.Currency)"
'

echo ""
echo "--- 详细账单 ---"
echo "$BILL_DATA" | jq '.'