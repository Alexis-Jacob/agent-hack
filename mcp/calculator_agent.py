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
from smolagents import ToolCollection

# ──────────────────────────────────────────────────────────────────────────────
# Configuration ----------------------------------------------------------------
LOCAL_MATH_SERVER = StdioServerParameters(
    command="python",
    args=[str(Path(__file__).with_name("calculator_server.py"))],   # ./math_server.py
)

REMOTE_CALCULATOR = {
    # Any Space launched with demo.launch(mcp_server=True) exposes this endpoint
    "url": "https://agents-mcp-hackathon-simple-calculator.hf.space/gradio_api/mcp/sse",
    "transport": "sse",
}


MODEL_ID = "mistralai/Mixtral-8x22B-Instruct-v0.1"   # works well for tool-use
HF_TOKEN = os.getenv("HF_TOKEN")                     # or login via `huggingface-cli login`
PROMPT = "What is (7 + 13) × 2?"                     # change as you like
# ──────────────────────────────────────────────────────────────────────────────


def build_model() -> InferenceClientModel:
    return InferenceClientModel(model_id=MODEL_ID, token=HF_TOKEN)


async def run_agent(tools_cfg, prompt: str) -> str:
    with ToolCollection.from_mcp(LOCAL_MATH_SERVER, trust_remote_code=True) as tool_collection:
        agent = CodeAgent(tools=[*tool_collection.tools], model=build_model(), add_base_tools=False)
        agent.run(PROMPT)


async def main():
    await run_agent(LOCAL_MATH_SERVER, PROMPT)


if __name__ == "__main__":
    asyncio.run(main())
