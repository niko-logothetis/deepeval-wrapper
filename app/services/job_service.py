import uuid
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

from ..models.evaluation import (
    JobStatus,
    AsyncEvaluationResponse,
    TestCaseResult,
    EvaluationSummary,
    JobListResponse
)


class JobService:
    """Service for managing asynchronous evaluation jobs."""
    
    def __init__(self, use_redis: bool = False):
        # In-memory job storage - works great for single server deployments
        self._jobs: Dict[str, Dict[str, Any]] = {}
        self._job_lock = asyncio.Lock()
        self.use_redis = use_redis
    
    async def create_job(
        self,
        job_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a new evaluation job."""
        job_id = str(uuid.uuid4())
        
        async with self._job_lock:
            self._jobs[job_id] = {
                "job_id": job_id,
                "status": JobStatus.PENDING,
                "created_at": datetime.now(),
                "started_at": None,
                "completed_at": None,
                "job_name": job_name,
                "tags": tags or [],
                "metadata": metadata or {},
                "results": None,
                "summary": None,
                "error": None,
                "progress": {"current": 0, "total": 0, "percentage": 0.0},
            }
        
        return job_id
    
    async def update_job_status(
        self,
        job_id: str,
        status: JobStatus,
        error: Optional[str] = None
    ) -> None:
        """Update job status."""
        async with self._job_lock:
            if job_id not in self._jobs:
                raise ValueError(f"Job {job_id} not found")
            
            job = self._jobs[job_id]
            job["status"] = status
            
            if status == JobStatus.RUNNING and job["started_at"] is None:
                job["started_at"] = datetime.now()
            elif status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
                job["completed_at"] = datetime.now()
            
            if error:
                job["error"] = error
    
    async def update_job_progress(
        self,
        job_id: str,
        current: int,
        total: int,
        message: Optional[str] = None
    ) -> None:
        """Update job progress."""
        async with self._job_lock:
            if job_id not in self._jobs:
                return
            
            job = self._jobs[job_id]
            percentage = (current / total * 100) if total > 0 else 0.0
            
            job["progress"] = {
                "current": current,
                "total": total,
                "percentage": round(percentage, 2),
                "message": message,
                "updated_at": datetime.now().isoformat()
            }
    
    async def complete_job(
        self,
        job_id: str,
        results: List[TestCaseResult],
        summary: EvaluationSummary
    ) -> None:
        """Mark job as completed with results."""
        async with self._job_lock:
            if job_id not in self._jobs:
                raise ValueError(f"Job {job_id} not found")
            
            job = self._jobs[job_id]
            job["status"] = JobStatus.COMPLETED
            job["completed_at"] = datetime.now()
            job["results"] = [result.dict() for result in results]  # Serialize for storage
            job["summary"] = summary.dict()
            job["progress"]["current"] = job["progress"]["total"]
            job["progress"]["percentage"] = 100.0
    
    async def fail_job(self, job_id: str, error: str) -> None:
        """Mark job as failed with error."""
        await self.update_job_status(job_id, JobStatus.FAILED, error)
    
    async def get_job(self, job_id: str) -> Optional[AsyncEvaluationResponse]:
        """Get job by ID."""
        async with self._job_lock:
            if job_id not in self._jobs:
                return None
            
            job_data = self._jobs[job_id].copy()
        
        # Convert stored results back to objects if they exist
        results = None
        summary = None
        
        if job_data["results"]:
            results = [TestCaseResult(**result_data) for result_data in job_data["results"]]
        
        if job_data["summary"]:
            summary = EvaluationSummary(**job_data["summary"])
        
        return AsyncEvaluationResponse(
            job_id=job_data["job_id"],
            status=job_data["status"],
            created_at=job_data["created_at"],
            started_at=job_data["started_at"],
            completed_at=job_data["completed_at"],
            job_name=job_data["job_name"],
            tags=job_data["tags"],
            results=results,
            summary=summary,
            error=job_data["error"],
            progress=job_data["progress"],
        )
    
    async def list_jobs(
        self,
        page: int = 1,
        page_size: int = 20,
        status_filter: Optional[JobStatus] = None,
        tag_filter: Optional[str] = None
    ) -> JobListResponse:
        """List jobs with pagination and filtering."""
        async with self._job_lock:
            jobs = list(self._jobs.values())
        
        # Apply filters
        if status_filter:
            jobs = [job for job in jobs if job["status"] == status_filter]
        
        if tag_filter:
            jobs = [job for job in jobs if tag_filter in job.get("tags", [])]
        
        # Sort by creation time (newest first)
        jobs.sort(key=lambda x: x["created_at"], reverse=True)
        
        # Apply pagination
        total = len(jobs)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_jobs = jobs[start_idx:end_idx]
        
        # Convert to response objects
        job_responses = []
        for job_data in page_jobs:
            job_response = AsyncEvaluationResponse(
                job_id=job_data["job_id"],
                status=job_data["status"],
                created_at=job_data["created_at"],
                started_at=job_data["started_at"],
                completed_at=job_data["completed_at"],
                job_name=job_data["job_name"],
                tags=job_data["tags"],
                results=None,  # Don't include full results in list view
                summary=None,  # Don't include full summary in list view
                error=job_data["error"],
                progress=job_data["progress"],
            )
            job_responses.append(job_response)
        
        return JobListResponse(
            jobs=job_responses,
            total=total,
            page=page,
            page_size=page_size
        )
    
    async def delete_job(self, job_id: str) -> bool:
        """Delete a job."""
        async with self._job_lock:
            if job_id in self._jobs:
                del self._jobs[job_id]
                return True
            return False
    
    async def cancel_job(self, job_id: str) -> bool:
        """Cancel a running job."""
        async with self._job_lock:
            if job_id not in self._jobs:
                return False
            
            job = self._jobs[job_id]
            if job["status"] in [JobStatus.PENDING, JobStatus.RUNNING]:
                job["status"] = JobStatus.CANCELLED
                job["completed_at"] = datetime.now()
                return True
            
            return False
    
    async def cleanup_old_jobs(self, max_age_days: int = 7) -> int:
        """Clean up old completed/failed jobs."""
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        deleted_count = 0
        
        async with self._job_lock:
            jobs_to_delete = []
            for job_id, job_data in self._jobs.items():
                if (job_data["status"] in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED] and
                    job_data["completed_at"] and job_data["completed_at"] < cutoff_date):
                    jobs_to_delete.append(job_id)
            
            for job_id in jobs_to_delete:
                del self._jobs[job_id]
                deleted_count += 1
        
        return deleted_count
    
    def get_job_stats(self) -> Dict[str, Any]:
        """Get statistics about jobs."""
        stats = {
            "total_jobs": len(self._jobs),
            "by_status": {},
            "recent_jobs": 0,  # Last 24 hours
        }
        
        recent_cutoff = datetime.now() - timedelta(hours=24)
        
        for job_data in self._jobs.values():
            status = job_data["status"]
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
            
            if job_data["created_at"] > recent_cutoff:
                stats["recent_jobs"] += 1
        
        return stats
