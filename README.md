# DeepEval API Wrapper

## What is DeepEval?

[DeepEval](https://github.com/confident-ai/deepeval) is the leading open-source LLM evaluation framework with over 10,500 stars on GitHub. 

Built by the team at Confident AI, DeepEval provides a comprehensive suite of 25+ research-backed metrics for evaluating Large Language Model applications. 

From RAG systems to conversational AI, DeepEval offers metrics for faithfulness, answer relevancy, contextual precision, bias detection, toxicity screening, and much more - making it the go-to solution for developers who need reliable, human-like accuracy in their LLM evaluations.

## The Wrapper

This REST API wrapper brings DeepEval's powerful evaluation capabilities to any application through simple HTTP endpoints. 

Whether you're building n8n AI agents, automated testing pipelines, or integrating LLM evaluation into existing systems, this wrapper provides an easy-to-deploy solution.

## 🚀 Quick Deploy to Render

### 1. Prerequisites
- GitHub repository with this code
- Render.com account (free tier works)
- OpenAI API key

### 2. Deploy Steps

**Deploy on Render:**
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "Web Service"
3. Paste in this public GitHub repository - https://github.com/theaiautomators/deepeval-wrapper
4. Render auto-detects Docker configuration
5. Click "Connect"

**Set Environment Variables:**
Add these environment variables:

**LLM Provider Keys:**
- `OPENAI_API_KEY` - Your OpenAI API key (required for most metrics)
- `ANTHROPIC_API_KEY` - Optional for Claude models  
- `GOOGLE_API_KEY` - Optional for Gemini models

**Authentication:**
- `API_KEYS` - API keys for accessing the API. Set something secure here

### 3. Test Your Deployment

Once deployed, your API will be available at : `https://your-app.onrender.com`

Visit your deployed API for interactive docs:
- **Swagger UI**: `https://your-app.onrender.com/docs`
- **ReDoc**: `https://your-app.onrender.com/redoc`

## 📊 Example Usage

### Simple Evaluation

```bash
curl -X POST "https://your-app.onrender.com/evaluate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "test_case": {
      "input": "What are the benefits of renewable energy?",
      "actual_output": "I really enjoy pizza on weekends. My favorite toppings are pepperoni and mushrooms."
    },
    "metrics": [
      {
        "metric_type": "answer_relevancy",
        "threshold": 0.7
      }
    ]
  }'
```
## Example n8n Workflows

There are two example n8n workflows in the n8n folder of the repo.

You can import these into n8n to test out some of the DeepEval metrics and how the flow would look from triggering to evaluating when testing your agents or systems.

## 🎯 DeepEval Metrics

- **RAG Metrics**: Faithfulness, Answer Relevancy, Contextual Precision/Recall/Relevancy
- **Safety Metrics**: Bias, Toxicity, Hallucination, PII Leakage  
- **Task Metrics**: Summarization, Tool Correctness, Task Completion
- **Custom**: G-Eval for custom criteria
- **Conversational**: Turn Relevancy, Conversation Completeness

For a full list of metrics, check out https://deepeval.com/docs/metrics-introduction

## ⚠️ Early Version Notice

This is an early version of the DeepEval API wrapper. While the core functionality works well, not all features of the DeepEval system have been fully tested in this wrapper format. 

**We're looking for experienced Python developers to help maintain and improve this project!** If you'd like to contribute or help maintain this wrapper, please get in touch - your expertise would be greatly appreciated.

<p align="center">
  <img src="https://www.theaiautomators.com/wp-content/uploads/2025/07/Group-2652.png" alt="The AI Automators Logo" width="500"/>
</p>

## Join Our Community

If you're interested in learning how to use and this DeepEval Wrapper for your n8n AI Agents, join our community, The AI Automators.

https://www.theaiautomators.com/

## 🤝 Contributing

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This codebase is distributed under the MIT License.