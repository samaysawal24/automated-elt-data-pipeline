"""
Unit tests for Automated ELT Data Pipeline
Author: Samay Sawal <cricketworldsamay@gmail.com>
"""

import pytest
from pipeline import (
    ELTPipelineRunner,
    RawDataExtractor,
    DataTransformer,
    DataQualityAuditor,
    EnrichedEvent
)


def test_bronze_extraction():
    batch = RawDataExtractor.generate_bronze_batch(count=20)
    assert len(batch) == 20
    assert batch[0].event_id.startswith("evt_")
    assert "country" in batch[0].properties


def test_silver_transformation_and_quality():
    batch = RawDataExtractor.generate_bronze_batch(count=30)
    silver = DataTransformer.bronze_to_silver(batch)
    assert len(silver) == 30
    assert isinstance(silver[0].revenue_usd, float)

    quality_results = DataQualityAuditor.audit_silver_table(silver)
    assert all(q.passed for q in quality_results)


def test_quality_auditor_catches_errors():
    corrupted_data = [
        EnrichedEvent(
            event_id="dup_1",
            user_id="user_a",
            event_name="page_view",
            revenue_usd=10.0,
            country="US",
            device_category="desktop",
            event_date="2026-11-03"
        ),
        EnrichedEvent(
            event_id="dup_1",  # duplicate ID
            user_id="",       # null user
            event_name="checkout",
            revenue_usd=-50.0, # negative revenue
            country="US",
            device_category="desktop",
            event_date="2026-11-03"
        )
    ]

    checks = DataQualityAuditor.audit_silver_table(corrupted_data)
    assert not all(c.passed for c in checks)
    failed_checks = [c.check_name for c in checks if not c.passed]
    assert "assert_unique_event_id" in failed_checks
    assert "assert_not_null_user_id" in failed_checks
    assert "assert_non_negative_revenue" in failed_checks


def test_end_to_end_pipeline_runner():
    summary = ELTPipelineRunner.run_pipeline(batch_size=25)
    assert summary.bronze_rows_ingested == 25
    assert summary.silver_rows_transformed == 25
    assert summary.all_quality_checks_passed is True
    assert summary.gold_metrics["total_revenue_usd"] >= 0.0

