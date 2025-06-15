from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ninja import NinjaAPI, Schema
from typing import Optional
from smolagents import CodeAgent, MCPClient
from smolagents.models import InferenceClientModel   # Hugging Face Inference API wrapper
from smolagents import ToolCollection, LiteLLMModel
# Create your views here.

api = NinjaAPI()

class ChatRequest(Schema):
    message: str

class ChatResponse(Schema):
    message: str


REMOTE_MCP = {
    "url": "http://mcp:5000/mcp/",
    "transport": "streamable-http",
}

def build_model() -> InferenceClientModel:
    """
    Available models are : 
    claude-4 (claude-opus-4-20250514, claude-sonnet-4-20250514)
    claude-3.7 (claude-3-7-sonnet-20250219)
    claude-3.5 (claude-3-5-sonnet-20240620)
    claude-3 (claude-3-haiku-20240307, claude-3-opus-20240229, claude-3-sonnet-20240229)

    You need to have the ANTHROPIC_API_KEY in your .env

    Here are the links:
    - https://docs.litellm.ai/docs/providers/anthropic
    - https://huggingface.co/docs/smolagents/en/index#using-different-models
    """
    return LiteLLMModel(model_id="claude-sonnet-4-20250514", api_key="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")


async def run_agent(tools_cfg, prompt: str) -> str:
    mcp_client = MCPClient(tools_cfg)
    with MCPClient(tools_cfg) as mcp_client:
        tools = mcp_client.get_tools()

        # Use the tools with your agent
        agent = CodeAgent(tools=tools, model=build_model())
        result = agent.run(prompt)

        return result


@api.post("/chat", response=ChatResponse)
async def chat(request, payload: ChatRequest):
    # Simulate some async operation (like database query or external API call)
    # await asyncio.sleep(0.1)  # Uncomment if you want to simulate async delay

    response = await run_agent(REMOTE_MCP, payload.message)
    response = str(response)
    return {"message": f"LLM: {response}"}
