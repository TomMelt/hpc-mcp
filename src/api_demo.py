
""" 
demo for mcp tool use via llm api 

assumes the mcp server is already running:
mcp = FastMCP(name=mcp_server_name)
mcp.run(transport="http")

"""

import os
import llm_api

# llm api config
api_url = "https://openrouter.ai/api/v1/chat/completions"
api_key = os.getenv("OPENROUTER_API_KEY")
model_name = "mistralai/mistral-nemo:free"

# mcp tool config
mcp_server_name = "DebugCrash"
mcp_url = "http://127.0.0.1:8000/mcp/"
mcp_tool_name = "debug_crash"
mcp_tool_description = "This tool will debug a crashing program and return the stack trace"
mcp_property_name = "path_to_executable"
mcp_property_description = "Path to the target executable that crashes when run"

# llm prompt config
llm_prompt = "Can you debug a crash in this program: "+os.getenv("PATH_TO_CRASH_FILE")

# mcp request
response = llm_api.mcp_request(api_url, api_key, model_name, mcp_url, mcp_tool_name, mcp_tool_description, mcp_property_name, mcp_property_description, llm_prompt)

print(); print(response)

