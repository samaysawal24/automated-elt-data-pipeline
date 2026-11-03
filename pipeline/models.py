"""
Data models and schemas for Modern ELT Data Pipeline
Author: Samay Sawal <cricketworldsamay@gmail.com>
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class RawEventRecord(BaseModel):
    event_id: str
    user_id: str
    event_name: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str


class EnrichedEvent(BaseModel):
    event_id: str
    user_id: str
    event_name: str
    revenue_usd: float
    country: str
    device_category: str
    event_date: str
    processed_at: datetime = Field(default_factory=datetime.utcnow)


class QualityCheckResult(BaseModel):
    check_name: str
    table_name: str
    passed: bool
    details: str
    records_checked: int


class PipelineRunSummary(BaseModel):
    run_id: str
    bronze_rows_ingested: int
    silver_rows_transformed: int
    gold_metrics: Dict[str, Any]
    quality_checks: List[QualityCheckResult]
    all_quality_checks_passed: bool
    execution_time_seconds: float
    completed_at: datetime = Field(default_factory=datetime.utcnow)

