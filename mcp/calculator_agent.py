#!/usr/bin/env python
"""
client.py – small-agent + MCP demo
Run with:
    python client.py                        # -> local ./math_server.py
    python client.py --remote               # -> remote HF Space
"""
import asyncio
import argparse
import os
from pathlib import Path

from mcp import StdioServerParameters           # stdio helper for local tools
from smolagents import CodeAgent, MCPClient
from smolagents.models import InferenceClientModel   # Hugging Face Inference API wrapper
from smolagents import ToolCollection, LiteLLMModel

# ──────────────────────────────────────────────────────────────────────────────
# Configuration ----------------------------------------------------------------
LOCAL_MATH_SERVER = StdioServerParameters(
    command="python",
    args=[str(Path(__file__).with_name("calculator_server.py"))],   # ./math_server.py
)

REMOTE_CALCULATOR = {
    # Any Space launched with demo.launch(mcp_server=True) exposes this endpoint
    "url": "http://localhost:5000/mcp/",
    "transport": "streamable-http",
}


MODEL_ID = "mistralai/Mixtral-8x22B-Instruct-v0.1"   # works well for tool-use
HF_TOKEN = os.getenv("HF_TOKEN")                     # or login via `huggingface-cli login`
PROMPT = "What is (7 + 13) × 2?"     

# ──────────────────────────────────────────────────────────────────────────────


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
    return LiteLLMModel(model_id="claude-3-7-sonnet-20250219", api_key="")    


async def run_agent(tools_cfg, prompt: str) -> str:
    with ToolCollection.from_mcp(REMOTE_CALCULATOR, trust_remote_code=True) as tool_collection:
        agent = CodeAgent(tools=[*tool_collection.tools], model=build_model(), add_base_tools=False)
        agent.run(PROMPT)


async def main():
    await run_agent(REMOTE_CALCULATOR, PROMPT)


if __name__ == "__main__":
    asyncio.run(main())
