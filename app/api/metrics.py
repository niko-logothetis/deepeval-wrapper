from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any

from ..models.auth import User
from ..models.metrics import MetricType, MetricInfo
from ..services.deepeval_service import DeepEvalService
from ..auth import get_current_user

router = APIRouter(prefix="/metrics", tags=["Metrics"])
deepeval_service = DeepEvalService()


@router.get("/", response_model=List[Dict[str, Any]])
async def list_available_metrics(current_user: User = Depends(get_current_user)):
    """List all available metrics."""
    metrics = deepeval_service.list_available_metrics()
    
    # Remove non-serializable class objects
    serializable_metrics = []
    for metric in metrics:
        serializable_metric = {k: v for k, v in metric.items() if k != "class"}
        serializable_metrics.append(serializable_metric)
    
    return serializable_metrics


@router.get("/categories")
async def list_metric_categories(current_user: User = Depends(get_current_user)):
    """List metric categories."""
    metrics = deepeval_service.list_available_metrics()
    categories = {}
    
    for metric in metrics:
        category = metric["category"]
        if category not in categories:
            categories[category] = {
                "name": category.title(),
                "description": _get_category_description(category),
                "metrics": []
            }
        categories[category]["metrics"].append({
            "metric_type": metric["metric_type"],
            "name": metric["name"],
            "supports_multimodal": metric["supports_multimodal"],
            "supports_conversational": metric["supports_conversational"],
        })
    
    return categories


@router.get("/{metric_type}")
async def get_metric_info(metric_type: MetricType, current_user: User = Depends(get_current_user)):
    """Get detailed information about a specific metric."""
    try:
        info = deepeval_service.get_metric_info(metric_type)
        # Remove non-serializable class object
        serializable_info = {k: v for k, v in info.items() if k != "class"}
        return {
            **serializable_info,
            "description": _get_metric_description(metric_type),
            "example_usage": _get_metric_example(metric_type),
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


def _get_category_description(category: str) -> str:
    """Get description for metric category."""
    descriptions = {
        "rag": "Metrics for evaluating Retrieval-Augmented Generation systems",
        "safety": "Metrics for detecting harmful, biased, or inappropriate content",
        "task": "Metrics for evaluating task-specific performance",
        "behavioral": "Metrics for evaluating adherence to roles and guidelines",
        "conversational": "Metrics for evaluating multi-turn conversations",
        "custom": "Customizable metrics using LLM-as-a-judge",
        "arena": "Metrics for comparing multiple model outputs",
        "multimodal": "Metrics for evaluating vision and multimodal models",
    }
    return descriptions.get(category, "General evaluation metrics")


def _get_metric_description(metric_type: MetricType) -> str:
    """Get detailed description for specific metric."""
    descriptions = {
        MetricType.FAITHFULNESS: "Measures how faithful the actual output is to the retrieval context by detecting contradictions and hallucinations.",
        MetricType.ANSWER_RELEVANCY: "Evaluates how relevant and helpful the response is to the input query.",
        MetricType.CONTEXTUAL_PRECISION: "Measures the precision of retrieved context - whether relevant information appears early in the context.",
        MetricType.CONTEXTUAL_RECALL: "Measures the recall of retrieved context - whether all necessary information is present.",
        MetricType.CONTEXTUAL_RELEVANCY: "Evaluates whether the retrieved context is relevant to the input query.",
        MetricType.BIAS: "Detects various types of bias in the model output including gender, racial, religious, and other biases.",
        MetricType.TOXICITY: "Identifies toxic, harmful, or inappropriate content in the model output.",
        MetricType.HALLUCINATION: "Detects when the model generates information not supported by the provided context.",
        MetricType.G_EVAL: "Custom metric using LLM-as-a-judge with user-defined criteria for evaluation.",
        # Add more descriptions as needed
    }
    return descriptions.get(metric_type, "Evaluation metric for LLM outputs.")


def _get_metric_example(metric_type: MetricType) -> Dict[str, Any]:
    """Get example usage for specific metric."""
    examples = {
        MetricType.FAITHFULNESS: {
            "test_case": {
                "input": "What is the capital of France?",
                "actual_output": "The capital of France is Paris.",
                "retrieval_context": ["Paris is the capital and largest city of France."]
            },
            "metric_config": {
                "metric_type": "faithfulness",
                "threshold": 0.8,
                "model": "gpt-4",
                "include_reason": True
            }
        },
        MetricType.G_EVAL: {
            "test_case": {
                "input": "Explain photosynthesis",
                "actual_output": "Photosynthesis is the process by which plants convert sunlight into energy.",
                "expected_output": "Photosynthesis is the biological process where plants use sunlight, water, and CO2 to produce glucose and oxygen."
            },
            "metric_config": {
                "metric_type": "g_eval",
                "name": "Scientific Accuracy",
                "criteria": "Evaluate the scientific accuracy and completeness of the explanation",
                "evaluation_params": ["actual_output", "expected_output"],
                "threshold": 0.7
            }
        }
    }
    
    return examples.get(metric_type, {
        "test_case": {"input": "Sample input", "actual_output": "Sample output"},
        "metric_config": {"metric_type": metric_type.value, "threshold": 0.5}
    })
