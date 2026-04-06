#!/usr/bin/env python3
"""
阿里云账单查询工具

使用阿里云 CLI 获取账号级账单信息，默认上个月
"""

import subprocess
import json
import os
from datetime import datetime
from typing import Optional


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

    def get_split_item_bill(self, billing_cycle: str) -> dict:
        return self.run_aliyun_cli([
            "bssopenapi", "describe-split-item-bill",
            "--billing-cycle", billing_cycle
        ])

    def get_account_balance(self) -> dict:
        return self.run_aliyun_cli([
            "bssopenapi", "query-account-balance"
        ])

    def print_report(self, billing_cycle: str):
        print("=" * 50)
        print("阿里云账单报告")
        print("=" * 50)
        print(f"计费周期: {billing_cycle}")
        print(f"区域: {self.region}")
        print()

        print("--- 实例账单 ---")
        bill = self.get_instance_bill(billing_cycle)
        if "error" not in bill:
            print(json.dumps(bill, indent=2, ensure_ascii=False))
        else:
            print(f"错误: {bill.get('error')}")
        print()

        print("--- 分账账单 ---")
        split_bill = self.get_split_item_bill(billing_cycle)
        if "error" not in split_bill:
            print(json.dumps(split_bill, indent=2, ensure_ascii=False))
        else:
            print(f"错误: {split_bill.get('error')}")
        print()

        print("--- 账户余额 ---")
        balance = self.get_account_balance()
        if "error" not in balance and "Data" in balance:
            data = balance["Data"]
            print(f"可用余额: {data.get('AvailableAmount')} {data.get('Currency')}")
            print(f"信用额度: {data.get('CreditAmount')} {data.get('Currency')}")
        else:
            print(json.dumps(balance, indent=2, ensure_ascii=False))


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