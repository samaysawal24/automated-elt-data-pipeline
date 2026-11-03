"""
Pipeline Orchestrator Runner
Author: smay <cricketworldsamay@gmail.com>
"""

import time
import uuid
from .models import PipelineRunSummary
from .extract import RawDataExtractor
from .transform import DataTransformer
from .quality import DataQualityAuditor


class ELTPipelineRunner:
    """
    Coordinates Bronze Ingestion -> Silver Cleaning -> Data Quality Test -> Gold Mart Export.
    """

    @classmethod
    def run_pipeline(cls, batch_size: int = 50) -> PipelineRunSummary:
        start_time = time.time()
        run_id = f"run_{uuid.uuid4().hex[:8]}"

        # 1. Bronze Ingestion
        bronze_records = RawDataExtractor.generate_bronze_batch(count=batch_size)

        # 2. Silver Transformation
        silver_records = DataTransformer.bronze_to_silver(bronze_records)

        # 3. Data Quality Gate
        quality_results = DataQualityAuditor.audit_silver_table(silver_records)
        all_passed = all(q.passed for q in quality_results)

        # 4. Gold Mart Aggregation
        gold_marts = DataTransformer.silver_to_gold_marts(silver_records)

        elapsed = time.time() - start_time

        return PipelineRunSummary(
            run_id=run_id,
            bronze_rows_ingested=len(bronze_records),
            silver_rows_transformed=len(silver_records),
            gold_metrics=gold_marts,
            quality_checks=quality_results,
            all_quality_checks_passed=all_passed,
            execution_time_seconds=round(elapsed, 3)
        )
