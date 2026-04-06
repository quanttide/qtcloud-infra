#!/usr/bin/env python3
"""
阿里云账单查询工具

使用阿里云 CLI 获取账号级账单信息
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
            print(f"CLI Error: {result.stderr}")
            return {}
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {}

    def get_bill_overview(self, billing_cycle: str) -> dict:
        return self.run_aliyun_cli([
            "bssapi", "QueryBillOverviewBill",
            "--BillingCycle", billing_cycle,
            "--Granularity", "MONTHLY"
        ])

    def get_bill_list(self, billing_cycle: str, max_results: int = 100) -> dict:
        return self.run_aliyun_cli([
            "bssapi", "QueryBillList",
            "--BillingCycle", billing_cycle,
            "--Granularity", "MONTHLY",
            "--MaxResults", str(max_results)
        ])

    def get_bill_detail(self, billing_cycle: str, product_code: str = None) -> dict:
        cmd = [
            "bssapi", "QueryBillDetail",
            "--BillingCycle", billing_cycle
        ]
        if product_code:
            cmd.extend(["--ProductCode", product_code])
        return self.run_aliyun_cli(cmd)

    def get_account_balance(self) -> dict:
        return self.run_aliyun_cli(["bssapi", "QueryAccountBalance"])

    def print_report(self, billing_cycle: str):
        print("=" * 50)
        print("阿里云账单报告")
        print("=" * 50)
        print(f"计费周期: {billing_cycle}")
        print(f"区域: {self.region}")
        print()

        print("--- 账户余额 ---")
        balance = self.get_account_balance()
        if balance:
            print(json.dumps(balance, indent=2, ensure_ascii=False))
        print()

        print("--- 账单概览 ---")
        overview = self.get_bill_overview(billing_cycle)
        if overview:
            print(json.dumps(overview, indent=2, ensure_ascii=False))
        print()

        print("--- 详细账单 ---")
        bills = self.get_bill_list(billing_cycle)
        if bills:
            print(json.dumps(bills, indent=2, ensure_ascii=False))
        print()

        print("--- 函数计算 (FC) 账单 ---")
        fc_bill = self.get_bill_detail(billing_cycle, "fc")
        if fc_bill:
            print(json.dumps(fc_bill, indent=2, ensure_ascii=False))
        print()


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
