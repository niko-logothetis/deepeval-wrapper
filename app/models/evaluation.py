from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

from .test_cases import (
    LLMTestCaseRequest,
    ConversationalTestCaseRequest,
    MLLMTestCaseRequest,
    ArenaTestCaseRequest,
)
from .metrics import MetricRequest, MetricResult


class JobStatus(str, Enum):
    """Status of an evaluation job."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TestCaseResult(BaseModel):
    """Result of evaluating a single test case."""
    test_case: Union[
        LLMTestCaseRequest,
        ConversationalTestCaseRequest,
        MLLMTestCaseRequest,
        ArenaTestCaseRequest,
    ]
    metrics: List[MetricResult]
    overall_success: bool
    execution_time: Optional[float] = None  # in seconds
    
    # For arena test cases
    winner: Optional[str] = None


class EvaluationSummary(BaseModel):
    """Summary statistics for batch evaluations."""
    total_test_cases: int
    successful_test_cases: int
    failed_test_cases: int
    success_rate: float
    total_execution_time: Optional[float] = None
    
    # Per-metric summaries
    metric_summaries: Dict[str, Dict[str, Any]] = {}


class EvaluationRequest(BaseModel):
    """Request for evaluating a single test case."""
    test_case: Union[
        LLMTestCaseRequest,
        ConversationalTestCaseRequest,
        MLLMTestCaseRequest,
        ArenaTestCaseRequest,
    ]
    metrics: List[MetricRequest]
    
    # Evaluation configuration
    run_async: Optional[bool] = True
    ignore_errors: Optional[bool] = False
    verbose_mode: Optional[bool] = False
    
    # Job configuration
    job_name: Optional[str] = None
    tags: Optional[List[str]] = None


class BulkEvaluationRequest(BaseModel):
    """Request for evaluating multiple test cases."""
    test_cases: List[Union[
        LLMTestCaseRequest,
        ConversationalTestCaseRequest,
        MLLMTestCaseRequest,
        ArenaTestCaseRequest,
    ]]
    metrics: List[MetricRequest]
    
    # Evaluation configuration
    run_async: Optional[bool] = True
    ignore_errors: Optional[bool] = True
    verbose_mode: Optional[bool] = False
    max_concurrent: Optional[int] = 10
    
    # Job configuration
    job_name: Optional[str] = None
    tags: Optional[List[str]] = None


class EvaluationResponse(BaseModel):
    """Response for single test case evaluation."""
    result: TestCaseResult
    execution_time: Optional[float] = None
    timestamp: datetime = datetime.now()


class BulkEvaluationResponse(BaseModel):
    """Response for bulk evaluation."""
    results: List[TestCaseResult]
    summary: EvaluationSummary
    execution_time: Optional[float] = None
    timestamp: datetime = datetime.now()


class AsyncEvaluationResponse(BaseModel):
    """Response for asynchronous evaluation jobs."""
    job_id: str
    status: JobStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Results (populated when completed)
    results: Optional[List[TestCaseResult]] = None
    summary: Optional[EvaluationSummary] = None
    error: Optional[str] = None
    
    # Job metadata
    job_name: Optional[str] = None
    tags: Optional[List[str]] = None
    progress: Optional[Dict[str, Any]] = None  # Progress tracking


class JobListResponse(BaseModel):
    """Response for listing evaluation jobs."""
    jobs: List[AsyncEvaluationResponse]
    total: int
    page: int
    page_size: int


class DatasetEvaluationRequest(BaseModel):
    """Request for evaluating a dataset from file."""
    dataset_name: str
    metrics: List[MetricRequest]
    
    # File processing options
    file_format: Optional[str] = "auto"  # "csv", "json", "auto"
    column_mapping: Optional[Dict[str, str]] = None  # Map file columns to test case fields
    
    # Evaluation configuration
    run_async: Optional[bool] = True
    ignore_errors: Optional[bool] = True
    max_concurrent: Optional[int] = 10
    
    # Job configuration
    job_name: Optional[str] = None
    tags: Optional[List[str]] = None
