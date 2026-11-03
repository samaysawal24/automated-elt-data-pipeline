"""
Bronze Layer: Raw Ingestion and Schema Extraction
Author: smay <cricketworldsamay@gmail.com>
"""

import uuid
from typing import List
from .models import RawEventRecord


class RawDataExtractor:
    """
    Extracts raw semi-structured JSON telemetry batches
    into Bronze staging partitions.
    """

    @classmethod
    def generate_bronze_batch(cls, count: int = 50) -> List[RawEventRecord]:
        events = []
        countries = ["US", "DE", "IN", "GB", "CA", "FR"]
        event_types = ["page_view", "add_to_cart", "checkout_completed", "search"]
        devices = ["desktop", "mobile", "tablet"]

        for i in range(1, count + 1):
            is_purchase = (i % 5 == 0)
            events.append(
                RawEventRecord(
                    event_id=f"evt_{uuid.uuid4().hex[:10]}",
                    user_id=f"usr_{100 + (i % 12)}",
                    event_name="checkout_completed" if is_purchase else event_types[i % len(event_types)],
                    properties={
                        "revenue": round(49.99 * ((i % 3) + 1), 2) if is_purchase else 0.0,
                        "country": countries[i % len(countries)],
                        "device": devices[i % len(devices)],
                    },
                    timestamp=f"2026-11-03T18:{i % 60:02d}:00Z"
                )
            )
        return events
