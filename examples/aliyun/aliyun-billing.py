#!/usr/bin/env python3
"""
阿里云账单查询工具

使用阿里云 CLI 获取账号级账单信息，默认上个月
"""

import subprocess
import json
import os
from datetime import datetime
from collections import defaultdict


class AliyunBilling:
    def __init__(self, region: str = None):
        self.region = region or os.getenv("ALIYUN_REGION", "cn-hangzhou")

    def run_aliyun_cli(self, command: list) -> dict:
        result = subprocess.run(
            ["aliyun"] + command,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return {"error": result.stderr}
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response"}

    def get_instance_bill(self, billing_cycle: str) -> dict:
        return self.run_aliyun_cli([
            "bssopenapi", "describe-instance-bill",
            "--billing-cycle", billing_cycle,
            "--granularity", "MONTHLY"
        ])

    def get_account_balance(self) -> dict:
        return self.run_aliyun_cli([
            "bssopenapi", "query-account-balance"
        ])

    def calculate_summary(self, bill_data: dict) -> tuple:
        if "error" in bill_data or "Data" not in bill_data:
            return {}, 0
        
        items = bill_data["Data"].get("Items", [])
        product_totals = defaultdict(float)
        total = 0
        
        for item in items:
            if item.get("Item") == "PayAsYouGoBill":
                amount = item.get("PretaxAmount", 0)
                product = item.get("ProductName", "未知")
                product_totals[product] += amount
                total += amount
        
        return dict(product_totals), total

    def print_report(self, billing_cycle: str):
        print("=" * 50)
        print("阿里云账单报告")
        print("=" * 50)
        print(f"计费周期: {billing_cycle}")
        print(f"区域: {self.region}")
        print()

        bill = self.get_instance_bill(billing_cycle)
        
        print("--- 账单汇总 ---")
        if "error" not in bill:
            product_totals, total = self.calculate_summary(bill)
            for product, amount in sorted(product_totals.items(), key=lambda x: -x[1]):
                print(f"  {product}: ¥{round(amount, 2)}")
            print()
            print("--- 总计 ---")
            print(f"  ¥{round(total, 2)}")
        else:
            print(f"错误: {bill.get('error')}")
        print()

        print("--- 账户余额 ---")
        balance = self.get_account_balance()
        if "error" not in balance and "Data" in balance:
            data = balance["Data"]
            print(f"  可用余额: ¥{data.get('AvailableAmount')} {data.get('Currency')}")
        else:
            print(f"错误: {balance.get('error', balance)}")
        print()

        print("--- 详细账单 ---")
        if "error" not in bill:
            print(json.dumps(bill, indent=2, ensure_ascii=False))


def get_last_month_cycle() -> str:
    now = datetime.now()
    if now.month == 1:
        return f"{now.year - 1}-12"
    return f"{now.year}-{now.month - 1:02d}"


def main():
    import argparse
    parser = argparse.ArgumentParser(description="阿里云账单查询")
    parser.add_argument("--region", default=os.getenv("ALIYUN_REGION", "cn-hangzhou"))
    parser.add_argument(
        "--period",
        default=get_last_month_cycle(),
        help=f"计费周期，格式 YYYY-MM，默认上月 ({get_last_month_cycle()})"
    )
    args = parser.parse_args()

    billing = AliyunBilling(region=args.region)
    billing.print_report(args.period)


if __name__ == "__main__":
    main()