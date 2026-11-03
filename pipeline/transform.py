"""
Silver & Gold Medallion SQL Transformation Layer
Author: smay <cricketworldsamay@gmail.com>
"""

from typing import List, Dict, Any
from .models import RawEventRecord, EnrichedEvent


class DataTransformer:
    """
    Transforms Bronze raw records into Silver cleaned facts
    and rolls up Gold dimensional aggregations.
    """

    @staticmethod
    def bronze_to_silver(raw_records: List[RawEventRecord]) -> List[EnrichedEvent]:
        silver_rows: List[EnrichedEvent] = []

        for r in raw_records:
            props = r.properties or {}
            silver_rows.append(
                EnrichedEvent(
                    event_id=r.event_id,
                    user_id=r.user_id,
                    event_name=r.event_name,
                    revenue_usd=float(props.get("revenue", 0.0)),
                    country=str(props.get("country", "UNKNOWN")),
                    device_category=str(props.get("device", "desktop")),
                    event_date=r.timestamp.split("T")[0]
                )
            )

        return silver_rows

    @staticmethod
    def silver_to_gold_marts(silver_rows: List[EnrichedEvent]) -> Dict[str, Any]:
        """Gold Layer: Executive KPIs, Revenue by Country, Device Breakdowns"""
        total_revenue = sum(row.revenue_usd for row in silver_rows)
        purchases = [row for row in silver_rows if row.event_name == "checkout_completed"]
        unique_users = set(row.user_id for row in silver_rows)

        revenue_by_country: Dict[str, float] = {}
        for p in purchases:
            revenue_by_country[p.country] = round(revenue_by_country.get(p.country, 0.0) + p.revenue_usd, 2)

        return {
            "total_revenue_usd": round(total_revenue, 2),
            "total_conversions": len(purchases),
            "unique_active_users": len(unique_users),
            "conversion_rate_percent": round((len(purchases) / max(1, len(silver_rows))) * 100, 2),
            "revenue_by_country": revenue_by_country,
        }
