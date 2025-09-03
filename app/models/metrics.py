from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from enum import Enum


class MetricType(str, Enum):
    """All available metric types in DeepEval."""
    
    # RAG Metrics
    FAITHFULNESS = "faithfulness"
    ANSWER_RELEVANCY = "answer_relevancy" 
    CONTEXTUAL_PRECISION = "contextual_precision"
    CONTEXTUAL_RECALL = "contextual_recall"
    CONTEXTUAL_RELEVANCY = "contextual_relevancy"
    
    # Safety & Bias Metrics
    BIAS = "bias"
    TOXICITY = "toxicity"
    HALLUCINATION = "hallucination"
    PII_LEAKAGE = "pii_leakage"
    
    # Task-Specific Metrics
    SUMMARIZATION = "summarization"
    TOOL_CORRECTNESS = "tool_correctness"
    TASK_COMPLETION = "task_completion"
    JSON_CORRECTNESS = "json_correctness"
    ARGUMENT_CORRECTNESS = "argument_correctness"
    
    # Behavioral Metrics
    ROLE_ADHERENCE = "role_adherence"
    ROLE_VIOLATION = "role_violation"
    NON_ADVICE = "non_advice"
    MISUSE = "misuse"
    PROMPT_ALIGNMENT = "prompt_alignment"
    KNOWLEDGE_RETENTION = "knowledge_retention"
    
    # Conversational Metrics
    TURN_RELEVANCY = "turn_relevancy"
    CONVERSATION_COMPLETENESS = "conversation_completeness"
    
    # Custom Metrics
    G_EVAL = "g_eval"
    CONVERSATIONAL_G_EVAL = "conversational_g_eval"
    
    # Multimodal Metrics
    MULTIMODAL_FAITHFULNESS = "multimodal_faithfulness"
    MULTIMODAL_ANSWER_RELEVANCY = "multimodal_answer_relevancy"
    MULTIMODAL_CONTEXTUAL_RELEVANCY = "multimodal_contextual_relevancy"
    TEXT_TO_IMAGE = "text_to_image"
    IMAGE_EDITING = "image_editing"
    
    # Arena Metrics
    ARENA_G_EVAL = "arena_g_eval"


class LLMTestCaseParam(str, Enum):
    """Parameters that can be used in metric evaluation."""
    INPUT = "input"
    ACTUAL_OUTPUT = "actual_output"
    EXPECTED_OUTPUT = "expected_output"
    CONTEXT = "context"
    RETRIEVAL_CONTEXT = "retrieval_context"
    TOOLS_CALLED = "tools_called"
    EXPECTED_TOOLS = "expected_tools"


class MetricRequest(BaseModel):
    """Request for a specific metric evaluation."""
    metric_type: MetricType
    
    # Common parameters for all metrics
    threshold: Optional[float] = 0.5
    model: Optional[str] = None  # "gpt-4", "claude-3-opus", etc.
    include_reason: Optional[bool] = True
    async_mode: Optional[bool] = True
    strict_mode: Optional[bool] = False
    verbose_mode: Optional[bool] = False
    
    # Metric-specific parameters
    
    # For FaithfulnessMetric
    truths_extraction_limit: Optional[int] = None
    
    # For G-Eval metrics
    name: Optional[str] = None
    criteria: Optional[str] = None
    evaluation_steps: Optional[List[str]] = None  # Alternative to criteria (mutually exclusive)
    evaluation_params: Optional[List[LLMTestCaseParam]] = None
    
    # For G-Eval rubric support
    rubric: Optional[List[Dict[str, Any]]] = None  # List of score ranges and expected outcomes
    
    # For BiasMetric
    bias_types: Optional[List[str]] = None  # ["gender", "race", "religion", etc.]
    
    # For ToxicityMetric  
    toxicity_categories: Optional[List[str]] = None
    
    # For ToolCorrectnessMetric
    exact_match_tool_names: Optional[bool] = None
    exact_match_input_parameters: Optional[bool] = None
    exact_match_tool_output: Optional[bool] = None
    
    # For SummarizationMetric
    assessment_questions: Optional[List[str]] = None
    
    # For NonAdviceMetric
    advice_types: Optional[List[str]] = None  # ["financial", "medical", "legal", etc.]
    
    # For MisuseMetric
    domain: Optional[str] = None  # Domain/context for misuse detection
    
    # For RoleViolationMetric and RoleAdherenceMetric
    role: Optional[str] = None  # Expected role (e.g., "helpful assistant", "customer service agent")
    
    # For PromptAlignmentMetric
    prompt_instructions: Optional[str] = None  # Instructions that should be followed (e.g., "Reply in all uppercase")
    
    # Additional custom parameters
    additional_params: Optional[Dict[str, Any]] = {}


class MetricResult(BaseModel):
    """Result of a metric evaluation."""
    metric_type: str
    score: float
    threshold: float
    success: bool
    reason: Optional[str] = None
    error: Optional[str] = None
    
    # Additional result data
    score_breakdown: Optional[Dict[str, Any]] = None
    evaluation_model: Optional[str] = None
    evaluation_cost: Optional[float] = None
    verbose_logs: Optional[str] = None
    
    # For arena metrics
    winner: Optional[str] = None  # "Model A" or "Model B"


class MetricInfo(BaseModel):
    """Information about a specific metric."""
    metric_type: MetricType
    name: str
    description: str
    required_params: List[LLMTestCaseParam]
    optional_params: List[str]
    supports_async: bool
    supports_multimodal: bool
    supports_conversational: bool
    category: str  # "rag", "safety", "task", etc.
