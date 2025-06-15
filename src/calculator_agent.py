import asyncio, os
from smolagents import CodeAgent, MCPClient, InferenceClientModel
from mcp import StdioServerParameters      # only for local stdio servers

model = InferenceClientModel(
    model_id="mistralai/Mixtral-8x22B-Instruct-v0.1",  # any tool-calling model works
    hf_token=os.environ["HF_TOKEN"]                    # or leave unset if you’re already logged in
)

async def run_local():
    """Use the same local math_server.py you already have."""
    math_params = StdioServerParameters(
        command="python", args=["./math_server.py"],   # identical to your original
        env=os.environ
    )
    async with MCPClient(math_params) as tools:        # discovers the tools
        agent = CodeAgent(tools=tools, model=model, add_base_tools=True)
        result = await agent.run_async("What is (7 + 13) × 2?")
        print(result)

async def run_remote():
    """Hit a hosted calculator Space on the HF hub."""
    # Every Gradio Space launched with `mcp_server=True`
    # exposes an SSE endpoint at …/gradio_api/mcp/sse
    calc_space = {
        "url": "https://agents-mcp-hackathon-simple-calculator.hf.space/gradio_api/mcp/sse",
        "transport": "sse"
    }
    async with MCPClient(calc_space) as tools:
        agent = CodeAgent(tools=tools, model=model)
        result = await agent.run_async("What is (7 + 13) × 2?")
        print(result)

if __name__ == "__main__":
    asyncio.run(run_remote())        # or run_local()
