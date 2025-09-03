from typing import List, Optional, Dict, Any, Union, Literal
from pydantic import BaseModel, Field
from enum import Enum


class ToolCall(BaseModel):
    """Tool call representation matching DeepEval's ToolCall structure."""
    name: str
    description: Optional[str] = None
    reasoning: Optional[str] = None
    output: Optional[Any] = None
    input_parameters: Optional[Dict[str, Any]] = Field(
        None, serialization_alias="inputParameters"
    )


class Turn(BaseModel):
    """Conversation turn for multi-turn evaluations."""
    role: Literal["user", "assistant"]
    content: str
    scenario: Optional[str] = None
    expected_outcome: Optional[str] = None
    retrieval_context: Optional[List[str]] = None
    tools_called: Optional[List[ToolCall]] = None


class MLLMImage(BaseModel):
    """Multimodal image representation."""
    type: Literal["image"] = "image"
    url: str  # Can be local path or URL
    description: Optional[str] = None


class LLMTestCaseRequest(BaseModel):
    """Single-turn LLM test case matching DeepEval's LLMTestCase."""
    input: str
    actual_output: str
    expected_output: Optional[str] = None
    context: Optional[List[str]] = None
    retrieval_context: Optional[List[str]] = None
    tools_called: Optional[List[ToolCall]] = None
    expected_tools: Optional[List[ToolCall]] = None
    
    # Additional metadata
    name: Optional[str] = None
    additional_metadata: Optional[Dict[str, Any]] = None
    comments: Optional[str] = None
    tags: Optional[List[str]] = None


class ConversationalTestCaseRequest(BaseModel):
    """Multi-turn conversational test case."""
    turns: List[Turn]
    chatbot_role: Optional[str] = None
    scenario: Optional[str] = None
    user_description: Optional[str] = None
    expected_outcome: Optional[str] = None
    context: Optional[List[str]] = None
    
    # Additional metadata
    name: Optional[str] = None
    additional_metadata: Optional[Dict[str, Any]] = None
    comments: Optional[str] = None
    tags: Optional[List[str]] = None


class MLLMTestCaseRequest(BaseModel):
    """Multimodal (vision) test case."""
    input: List[Union[str, MLLMImage]]  # Mix of text and images
    actual_output: str
    expected_output: Optional[str] = None
    context: Optional[List[str]] = None
    retrieval_context: Optional[List[str]] = None
    tools_called: Optional[List[ToolCall]] = None
    expected_tools: Optional[List[ToolCall]] = None
    
    # Additional metadata
    name: Optional[str] = None
    additional_metadata: Optional[Dict[str, Any]] = None
    comments: Optional[str] = None
    tags: Optional[List[str]] = None


class ArenaTestCaseRequest(BaseModel):
    """Arena test case for model comparison."""
    input: str
    model_a_output: str
    model_b_output: str
    model_a_name: Optional[str] = "Model A"
    model_b_name: Optional[str] = "Model B"
    
    # Additional metadata
    name: Optional[str] = None
    additional_metadata: Optional[Dict[str, Any]] = None
    comments: Optional[str] = None
    tags: Optional[List[str]] = None


# Union type for all test case types
TestCaseRequest = Union[
    LLMTestCaseRequest,
    ConversationalTestCaseRequest, 
    MLLMTestCaseRequest,
    ArenaTestCaseRequest
]
