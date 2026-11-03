#!/usr/bin/env python3
"""
CLI entry point for Automated ELT Data Pipeline
Author: smay <cricketworldsamay@gmail.com>
"""

import sys
import argparse
from pipeline import ELTPipelineRunner


def main():
    parser = argparse.ArgumentParser(description="Automated ELT Pipeline CLI - smay")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Run command
    run_parser = subparsers.add_parser("run", help="Execute complete Medallion ELT pipeline")
    run_parser.add_argument("--batch-size", type=int, default=100, help="Number of records to extract & transform")

    args = parser.parse_args()

    if args.command == "run":
        print(f"\n[ELT Pipeline] Starting batch pipeline run (batch_size={args.batch_size})...")
        summary = ELTPipelineRunner.run_pipeline(batch_size=args.batch_size)

        print("\n=== ELT Pipeline Execution Summary ===")
        print(f"Run ID:                 {summary.run_id}")
        print(f"Bronze Ingested Rows:   {summary.bronze_rows_ingested:,}")
        print(f"Silver Cleaned Rows:    {summary.silver_rows_transformed:,}")
        print(f"Latency:                {summary.execution_time_seconds}s")
        print(f"Data Quality Gate:      {'PASSED' if summary.all_quality_checks_passed else 'FAILED'}")

        print("\n=== Data Quality Assertions ===")
        for q in summary.quality_checks:
            status = "PASS" if q.passed else "FAIL"
            print(f"  [{status}] {q.check_name:<30} | {q.details}")

        print("\n=== Gold Analytics KPI Mart ===")
        print(f"  Total Revenue:       ${summary.gold_metrics['total_revenue_usd']:,.2f}")
        print(f"  Total Conversions:   {summary.gold_metrics['total_conversions']:,}")
        print(f"  Conversion Rate:     {summary.gold_metrics['conversion_rate_percent']}%")
        print(f"  Unique Active Users: {summary.gold_metrics['unique_active_users']}")
        print(f"  Revenue by Country:  {summary.gold_metrics['revenue_by_country']}\n")


if __name__ == "__main__":
    main()
