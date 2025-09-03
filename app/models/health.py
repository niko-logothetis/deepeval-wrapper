from typing import Dict, Any, Optional
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response."""
    status: str  # "healthy", "unhealthy", "degraded"
    version: str
    timestamp: str
    
    # Service checks
    deepeval_available: bool
    redis_available: Optional[bool] = None
    
    # LLM provider availability
    openai_configured: bool
    anthropic_configured: Optional[bool] = None
    google_configured: Optional[bool] = None
    
    # System info
    system_info: Optional[Dict[str, Any]] = None
    uptime: Optional[float] = None  # in seconds
    
    # Error details (if unhealthy)
    errors: Optional[list] = None
