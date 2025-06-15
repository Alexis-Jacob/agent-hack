from django.shortcuts import render
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ninja import NinjaAPI, Schema
from typing import Optional, List
from smolagents import CodeAgent, MCPClient
from smolagents.models import InferenceClientModel   # Hugging Face Inference API wrapper
from smolagents import ToolCollection, LiteLLMModel
from django.core.cache import cache
import os
from datetime import datetime
import mimetypes
from .agents import run_agent
# Create your views here.

api = NinjaAPI()

class ChatRequest(Schema):
    message: str

class ChatResponse(Schema):
    message: str

class FileInfo(Schema):
    name: str
    size: int
    modified: str
    is_dir: bool

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
    return LiteLLMModel(model_id="claude-sonnet-4-20250514", api_key="")


# async def run_agent(tools_cfg, prompt: str) -> str:
#     with ToolCollection.from_mcp(tools_cfg, trust_remote_code=True) as tool_collection:
#         agent = CodeAgent(tools=[*tool_collection.tools], model=build_model(), add_base_tools=False)
        
#         # prompt formation
#         prompt += "please return me your response in a json format for me to be able to parse it"
#         result = agent.run(prompt)
#         return result
    # mcp_client = MCPClient([tools_cfg])
    # with MCPClient(tools_cfg) as mcp_client:
    #     tools = mcp_client.get_tools()

    #     # Use the tools with your agent
    #     agent = CodeAgent(tools=tools, model=build_model())
    #     result = agent.run(prompt)

    #     return result


@api.post("/chat", response=ChatResponse)
async def chat(request, payload: ChatRequest):
    history = cache.get("history", [])    
    history.append("My message: " + payload.message)
    cache.set("history", history)
    # Simulate some async operation (like database query or external API call)
    # await asyncio.sleep(0.1)  # Uncomment if you want to simulate async delay
    chat = ",".join(history)
    response = run_agent(REMOTE_MCP, chat)
    response = str(response)
    history.append("Your response: " + response)
    cache.set("history", history)
    return {"message": response}


@api.post("/new_chat")
def get_history(request):
    history = cache.delete("history")
    return {"message": "ok"}

@api.get("/files/{file_path}")
def serve_file(request, file_path: str):
    # Ensure the file path is within /tmp directory
    full_path = os.path.join("/tmp", file_path)
    
    # Security check to prevent directory traversal
    if not os.path.abspath(full_path).startswith("/tmp"):
        return HttpResponse("Access denied", status=403)
    
    if not os.path.exists(full_path):
        return HttpResponse("File not found", status=404)
    
    if os.path.isdir(full_path):
        return HttpResponse("Cannot serve directory", status=400)
    
    # Get the file's mime type
    content_type, _ = mimetypes.guess_type(full_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    
    # Serve the file
    response = FileResponse(open(full_path, 'rb'))
    response['Content-Type'] = content_type
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
    return response


