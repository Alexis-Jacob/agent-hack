from smolagents import CodeAgent, InferenceClientModel, Tool, Model, PromptTemplates

from pandas import DataFrame

from smolagents.models import InferenceClientModel   # Hugging Face Inference API wrapper
from smolagents import ToolCollection, LiteLLMModel
# Create your views here.
import os
import tempfile
import matplotlib.pyplot as plt
from smolagents import tool
import argparse

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


@tool
def save_matplotlib_graph_to_tmp() -> None:
    """
    Saves the current matplotlib figure to a uniquely named temporary PNG file.

        Returns:
            str: The file path of the saved temporary PNG file.
    """
    tmp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    plt.savefig(tmp_file.name)
    tmp_file.close()
    return tmp_file.name
    

def run_agent(tools_cfg, prompt: str) -> str:
    with ToolCollection.from_mcp(tools_cfg, trust_remote_code=True) as tool_collection:
        retriever_prompt="""
        While processing the following request, work with a DataFrame called working_df. 
        When you are done, convert the dataframe to json with working_df.to_json, and return it. 
        When ever you aquire data, you must aquire at least 100 posts, or comments.
        """

        agent_retriever = CodeAgent(tools=[*tool_collection.tools], model=build_model(), add_base_tools=False, additional_authorized_imports=["pandas", "pandas.*", "json"])
        data_extract = agent_retriever.run(retriever_prompt + f"\nuser request: {prompt}" )


        agent_analyzer = CodeAgent(tools=[], 
                                   model=build_model(), 
                                   add_base_tools=False, additional_authorized_imports=["pandas", "pandas.*", "json"])
        
        intereting_info = agent_analyzer.run("analyze this pandas dataset and give me interesting information.",
                            additional_args={
                                "dataframe": data_extract
                            })
        
        graph_agent = CodeAgent(tools=[*tool_collection.tools, save_matplotlib_graph_to_tmp], 
                          model=build_model(), 
                          add_base_tools=False, additional_authorized_imports=["pandas", "pandas.*", "json", "seaborn", "matplotlib.*"], )
        
        graph = graph_agent.run("come up with directions to represent this information as graphs"
                                "you are given a pandas frame as well as directions to make graphs out of this pandas frame"
                                "don't show the graph, just save it",
                            additional_args={
                                "dataframe": data_extract,
                                "directions": intereting_info
                            },
                            max_steps=5)

# run_agent(REMOTE_MCP, "what are most influenciatal users on r/politics ?")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run the agent with a user query.")
    parser.add_argument("-q", "--query", type=str, help="The user query to process")
    args = parser.parse_args()

    run_agent(REMOTE_MCP, args.query)


