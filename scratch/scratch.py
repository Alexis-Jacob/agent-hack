from smolagents import CodeAgent, InferenceClientModel, Tool, Model, PromptTemplates

from pandas import DataFrame

from smolagents.models import InferenceClientModel   # Hugging Face Inference API wrapper
from smolagents import ToolCollection, LiteLLMModel
# Create your views here.
import os


REMOTE_MCP = {
    "url": "http://localhost:5000/mcp/",
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
    return LiteLLMModel(model_id="claude-sonnet-4-20250514", api_key=os.environ['ANTHROPIC_API_KEY'])


def run_agent(tools_cfg, prompt: str) -> str:
    with ToolCollection.from_mcp(tools_cfg, trust_remote_code=True) as tool_collection:
        agent = CodeAgent(tools=[*tool_collection.tools], model=build_model(), add_base_tools=False)
        result = agent.run(prompt)
        return result
    # mcp_client = MCPClient([tools_cfg])
    # with MCPClient(tools_cfg) as mcp_client:
    #     tools = mcp_client.get_tools()

    #     # Use the tools with your agent
    #     agent = CodeAgent(tools=tools, model=build_model())
    #     result = agent.run(prompt)

    #     return result


run_agent(REMOTE_MCP, "give me the latest post on r/politics")