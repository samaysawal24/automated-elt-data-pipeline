"""
Data Quality Auditing & Assertion Suite
Author: smay <cricketworldsamay@gmail.com>
"""

from typing import List
from .models import EnrichedEvent, QualityCheckResult


class DataQualityAuditor:
    """
    Executes automated data quality gates equivalent to dbt test assertions:
    - Unique Primary Key
    - Non-null mandatory columns
    - Positive revenue constraints
    """

    @classmethod
    def audit_silver_table(cls, records: List[EnrichedEvent]) -> List[QualityCheckResult]:
        checks: List[QualityCheckResult] = []
        total = len(records)

        # 1. Uniqueness test on event_id
        seen_ids = set()
        duplicates = 0
        for r in records:
            if r.event_id in seen_ids:
                duplicates += 1
            seen_ids.add(r.event_id)

        checks.append(
            QualityCheckResult(
                check_name="assert_unique_event_id",
                table_name="silver_events",
                passed=(duplicates == 0),
                details=f"Found {duplicates} duplicate primary key IDs",
                records_checked=total
            )
        )

        # 2. Not-null test on user_id
        null_users = sum(1 for r in records if not r.user_id or r.user_id.strip() == "")
        checks.append(
            QualityCheckResult(
                check_name="assert_not_null_user_id",
                table_name="silver_events",
                passed=(null_users == 0),
                details=f"Found {null_users} null or empty user identifiers",
                records_checked=total
            )
        )

        # 3. Value Range test on revenue >= 0
        negative_rev = sum(1 for r in records if r.revenue_usd < 0.0)
        checks.append(
            QualityCheckResult(
                check_name="assert_non_negative_revenue",
                table_name="silver_events",
                passed=(negative_rev == 0),
                details=f"Found {negative_rev} records with negative currency values",
                records_checked=total
            )
        )

        return checks
